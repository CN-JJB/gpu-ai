#!/usr/bin/env python3
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]

GROUPS = {
    "foundations": (ROOT / "curriculum" / "foundations", "*.md", 6),
    "experiments": (ROOT / "labs" / "experiments", "[0-9]*/README.md", 93),
    "challenges": (ROOT / "labs" / "challenges", "[0-9]*/README.md", 12),
    "references": (ROOT / "reference", "*/*.md", 50),
}

HTML_IMG_RE = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', re.I)
ALT_RE = re.compile(r'\balt=["\']([^"\']*)["\']', re.I)
MD_IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+["\'][^"\']*["\'])?\)')
REMOTE_SCHEMES = ("http://", "https://", "data:", "blob:")


def local_target(page: Path, raw: str):
    raw = raw.strip().strip("<>")
    if not raw or raw.startswith("#") or raw.startswith(REMOTE_SCHEMES):
        return None
    raw = raw.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw:
        return None
    return (page.parent / unquote(raw)).resolve()


def inspect_page(page: Path, root_resolved: Path):
    errors = []
    local_refs = []
    text = page.read_text(encoding="utf-8")
    rel = page.relative_to(ROOT)

    for match in HTML_IMG_RE.finditer(text):
        src = match.group(1)
        target = local_target(page, src)
        if target is None:
            continue
        try:
            target.relative_to(root_resolved)
        except ValueError:
            errors.append(f"{rel}: image src escapes repo -> {src}")
            continue
        if not target.exists():
            errors.append(f"{rel}: broken image src -> {src}")
            continue
        alt_match = ALT_RE.search(match.group(0))
        if not alt_match or not alt_match.group(1).strip():
            errors.append(f"{rel}: local teaching image missing non-empty alt -> {src}")
        local_refs.append(src)

    for match in MD_IMG_RE.finditer(text):
        alt, src = match.group(1), match.group(2)
        target = local_target(page, src)
        if target is None:
            continue
        try:
            target.relative_to(root_resolved)
        except ValueError:
            errors.append(f"{rel}: markdown image escapes repo -> {src}")
            continue
        if not target.exists():
            errors.append(f"{rel}: broken markdown image -> {src}")
            continue
        if not alt.strip():
            errors.append(f"{rel}: local markdown teaching image missing non-empty alt -> {src}")
        local_refs.append(src)

    if not local_refs:
        errors.append(f"{rel}: no local visual teaching surface")
    elif "<figcaption" not in text.lower():
        errors.append(f"{rel}: local teaching visual present but no figcaption")

    return local_refs, errors


def main():
    errors = []
    root_resolved = ROOT.resolve()
    total_pages = 0
    total_visual_pages = 0
    total_local_refs = 0
    group_stats = {}

    for name, (base, pattern, expected) in GROUPS.items():
        pages = sorted(base.glob(pattern))
        total_pages += len(pages)
        visual_pages = 0
        local_refs = 0

        if len(pages) != expected:
            errors.append(f"{name}: expected {expected} pages, found {len(pages)}")

        for page in pages:
            refs, page_errors = inspect_page(page, root_resolved)
            errors.extend(page_errors)
            if refs:
                visual_pages += 1
                local_refs += len(refs)

        total_visual_pages += visual_pages
        total_local_refs += local_refs
        group_stats[name] = (len(pages), visual_pages, local_refs)

    print("AUXILIARY VISUAL / COMPREHENSION CLOSURE AUDIT")
    for name in ("foundations", "experiments", "challenges", "references"):
        pages, visual_pages, refs = group_stats[name]
        print(f"{name}_pages={pages}")
        print(f"{name}_visual_pages={visual_pages}")
        print(f"{name}_local_visual_refs={refs}")
    print(f"total_pages={total_pages}")
    print(f"pages_with_teaching_surface={total_visual_pages}")
    print(f"local_visual_refs={total_local_refs}")

    if errors:
        print(f"errors={len(errors)}")
        for error in errors:
            print("- " + error)
        print("AUXILIARY VISUAL / COMPREHENSION CLOSURE: BLOCKED")
        raise SystemExit(2)

    print("errors=0")
    print("AUXILIARY VISUAL / COMPREHENSION CLOSURE: PASS")


if __name__ == "__main__":
    main()
