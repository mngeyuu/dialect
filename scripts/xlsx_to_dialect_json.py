#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将「数据库新老派词汇对照」类 Excel 转为 dialect-words.json（供静态网页 / localStorage 使用）。

用法：
  python scripts/xlsx_to_dialect_json.py                    # 默认读项目根目录第一个 .xlsx
  python scripts/xlsx_to_dialect_json.py 路径/文件.xlsx      # 指定文件
  python scripts/xlsx_to_dialect_json.py -o out.json 某.xlsx # 指定输出
  python scripts/xlsx_to_dialect_json.py --merge 某.xlsx    # 与默认输出 JSON 按编号合并

依赖：pip install pandas openpyxl
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("请先安装: pip install pandas openpyxl", file=sys.stderr)
    sys.exit(1)

# 表头别名（列名匹配任一即使用该列）
COL_ALIASES = {
    "code": ["编号", "CODE", "code", "序号"],
    "word": ["词汇", "word", "WORD", "普通话"],
    "old_dialect_word": ["老派词汇", "老派"],
    "new_dialect_word": ["新派词汇", "新派"],
    "old_dialect_phonetic": ["老派记音", "老派音"],
    "new_dialect_phonetic": ["新派记音", "新派音"],
}


def find_column(df: "pd.DataFrame", key: str) -> str | None:
    aliases = COL_ALIASES[key]
    for c in df.columns:
        s = str(c).strip()
        if s in aliases:
            return c
    return None


def normalize_code(val) -> str:
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return ""
    if isinstance(val, (int, float)):
        n = int(val)
        return str(n).zfill(4)
    s = str(val).strip()
    if re.fullmatch(r"\d+\.0+", s):
        s = s.split(".")[0]
    if s.isdigit():
        return s.zfill(4)
    return s


def row_to_record(df: "pd.DataFrame", row_idx: int, colmap: dict) -> dict:
    row = df.iloc[row_idx]

    def get(col_key: str, default="") -> str:
        col = colmap.get(col_key)
        if col is None:
            return default
        v = row[col]
        if pd.isna(v):
            return default
        return str(v).strip()

    code = normalize_code(get("code", row_idx + 1))
    word = get("word")
    return {
        "id": row_idx + 1,
        "code": code or str(row_idx + 1).zfill(4),
        "word": word,
        "old_dialect_word": get("old_dialect_word"),
        "old_dialect_phonetic": get("old_dialect_phonetic"),
        "old_dialect_audio": "",
        "new_dialect_word": get("new_dialect_word"),
        "new_dialect_phonetic": get("new_dialect_phonetic"),
        "new_dialect_audio": "",
    }


def build_column_map(df: "pd.DataFrame") -> dict:
    colmap = {}
    for key in COL_ALIASES:
        c = find_column(df, key)
        if c is not None:
            colmap[key] = c
    # 若未匹配到，按常见四列顺序兜底
    if "code" not in colmap and len(df.columns) >= 4:
        cols = list(df.columns)
        colmap.setdefault("code", cols[0])
        colmap.setdefault("word", cols[1])
        colmap.setdefault("old_dialect_word", cols[2])
        colmap.setdefault("new_dialect_word", cols[3])
    return colmap


def xlsx_to_records(path: Path) -> list[dict]:
    df = pd.read_excel(path, dtype=object)
    df = df.dropna(how="all")
    colmap = build_column_map(df)
    if "word" not in colmap and "code" not in colmap:
        raise SystemExit(f"无法识别列名，当前列为: {list(df.columns)}")
    out = []
    for i in range(len(df)):
        rec = row_to_record(df, i, colmap)
        if not rec["word"] and not rec["old_dialect_word"] and not rec["new_dialect_word"]:
            continue
        out.append(rec)
    # 重新编号 id
    for i, r in enumerate(out):
        r["id"] = i + 1
    return out


def merge_by_code(existing: list[dict], incoming: list[dict]) -> list[dict]:
    """按 code 合并：同编号以 incoming 为准；再按 code 排序并重排 id。"""
    by_code: dict[str, dict] = {}
    for r in existing:
        c = str(r.get("code") or "").strip()
        if not c:
            continue
        by_code[c] = dict(r)
    for r in incoming:
        c = str(r.get("code") or "").strip()
        if not c:
            continue
        by_code[c] = dict(r)
    merged = list(by_code.values())

    def sort_key(rec: dict) -> tuple:
        c = str(rec.get("code") or "")
        return (int(c) if c.isdigit() else 10**9, c)

    merged.sort(key=sort_key)
    for i, r in enumerate(merged):
        r["id"] = i + 1
    return merged


def main():
    ap = argparse.ArgumentParser(description="Excel 转 dialect-words.json")
    ap.add_argument("xlsx", nargs="?", help="输入 .xlsx 路径")
    ap.add_argument(
        "-o",
        "--output",
        default="",
        help="输出 JSON 路径（默认: dialect-frontend/public/data/dialect-words.json）",
    )
    ap.add_argument(
        "--merge",
        action="store_true",
        help="与输出路径已有 JSON 按编号合并（同编号以本次 Excel 为准）",
    )
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent

    if args.xlsx:
        src = Path(args.xlsx).expanduser().resolve()
    else:
        cands = sorted(root.glob("*.xlsx")) + sorted(root.glob("*.XLSX"))
        cands = [p for p in cands if "data.xlsx" not in p.name.lower()]
        if not cands:
            print("项目根目录未找到 .xlsx，请指定文件路径。", file=sys.stderr)
            sys.exit(1)
        src = cands[0]
        print("使用:", src)

    if not src.is_file():
        print("文件不存在:", src, file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output) if args.output else root / "dialect-frontend/public/data/dialect-words.json"
    out_path = out_path.resolve()
    records = xlsx_to_records(src)
    if args.merge and out_path.is_file():
        try:
            old = json.loads(out_path.read_text(encoding="utf-8"))
            if isinstance(old, list):
                records = merge_by_code(old, records)
                print(f"已与现有 {len(old)} 条合并 -> 共 {len(records)} 条")
        except (json.JSONDecodeError, OSError) as e:
            print("合并失败，仅写入本次 Excel：", e, file=sys.stderr)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"已写入 {len(records)} 条 -> {out_path}")


if __name__ == "__main__":
    main()
