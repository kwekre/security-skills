# -*- coding: utf-8 -*-
"""
Security Skills 搜索 / 筛选工具
依赖：SKILL_FULL_REGISTRY.json（同目录）

用法:
  python search.py --list-cats                 # 列出所有分类及数量
  python search.py -c web-attack               # 按分类过滤
  python search.py -k sqli                     # 按关键词过滤（匹配 name/description）
  python search.py -c ctf -k crypto --limit 10 # 组合 + 限制条数
"""
import json
import argparse

REG = 'SKILL_FULL_REGISTRY.json'


def load():
    return json.load(open(REG, encoding='utf-8'))


def main():
    ap = argparse.ArgumentParser(description='Search security skills in this repo')
    ap.add_argument('-c', '--category', help='按分类过滤（如 web-attack / ctf / active-directory）')
    ap.add_argument('-k', '--keyword', help='关键词，匹配 name 或 description')
    ap.add_argument('-l', '--limit', type=int, default=20, help='最多显示条数（默认 20）')
    ap.add_argument('--list-cats', action='store_true', help='列出所有分类及数量')
    args = ap.parse_args()

    reg = load()
    skills = reg['skills']

    if args.list_cats:
        for cat, n in sorted(reg['categories'].items(), key=lambda x: -x[1]):
            print('%-22s %d' % (cat, n))
        print('---')
        print('total: %d skills / %d categories' % (reg['total'], len(reg['categories'])))
        return

    res = skills
    if args.category:
        res = [s for s in res if s['category'] == args.category]
    if args.keyword:
        kw = args.keyword.lower()
        res = [s for s in res if kw in s['name'].lower() or kw in (s.get('description') or '').lower()]
    matched = len(res)
    res = res[:args.limit]

    for s in res:
        desc = (s.get('description') or '')[:90]
        print('[%s] %s' % (s['category'], s['name']))
        print('  %s' % s['path'])
        if desc:
            print('  %s' % desc)
    print('---')
    print('matched: %d  |  showing: %d' % (matched, len(res)))


if __name__ == '__main__':
    main()
