"""Light consistency checks for a book's markdown: cross-references, footnotes, leftover markers, quote style, word counts.
Usage: python lint_book.py agi-transition
"""
import re, sys
from pathlib import Path

book = Path(__file__).resolve().parent / sys.argv[1]
files = sorted(book.glob("00-*.md")) + sorted(book.glob("ch*.md"), key=lambda p: int(re.match(r"ch(\d+)", p.name).group(1))) + sorted(book.glob("99-*.md"))
n_ch = len([f for f in files if f.name.startswith("ch")])
total = 0
problems = 0
for f in files:
    t = f.read_text(encoding="utf-8")
    words = len(t.split()); total += words
    issues = []
    for m in re.finditer(r"[Cc]hapters? (\d+)", t):
        line = t[t.rfind("\n", 0, m.start()) + 1: t.find("\n", m.end())]
        if "Site Reliability Engineering" in line:  # citing another book's chapter, not this one's
            continue
        if not 1 <= int(m.group(1)) <= 12: issues.append(f"bad chapter ref {m.group(0)}")
    refs = set(re.findall(r"\[\^(\w+)\](?!:)", t)); defs = set(re.findall(r"^\[\^(\w+)\]:", t, re.M))
    if refs - defs: issues.append(f"undefined footnotes {sorted(refs - defs)}")
    if defs - refs: issues.append(f"unused footnotes {sorted(defs - refs)}")
    for marker in ("TODO", "TBD", "<!--", "XXX", "[citation", "lorem"):
        if marker in t: issues.append(f"marker {marker!r} present")
    if re.search(r" {2,}\S", t.replace("\n", "")): issues.append("double spaces")
    if re.search(r"\bpercent\b", t): issues.append("'percent' (house style is 'per cent')")
    if re.search(r"\b(utilize|utilise|leverage[sd]?|delve|tapestry|testament to|game-changer|cutting-edge)\b", t, re.I): issues.append("slop word")
    if t.count("“") + t.count("”") > 0 and t.count('"') > 0: issues.append("mixed curly and straight quotes")
    if f.name.startswith("ch") and "## What would make this chapter wrong" not in t and "## The question you will be asked" not in t:
        issues.append("missing closing section")
    if f.name.startswith("ch") and not re.search(r"^### Sources for this chapter", t, re.M): issues.append("no sources section")
    status = "ok " if not issues else "!! "
    problems += len(issues)
    print(f"{status}{words:6d}  {f.name}" + (("  -> " + "; ".join(issues)) if issues else ""))
print(f"\n{n_ch} chapters, {total:,} words, {problems} issue(s)")
