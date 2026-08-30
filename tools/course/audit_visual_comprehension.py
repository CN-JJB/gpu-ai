#!/usr/bin/env python3
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "lessons"
EXPECTED_LESSON_HTML_COUNT = 62

IMG_RE = re.compile(r'<img\\b[^>]*\\bsrc=["\\']([^"\\']+)["\\'][^>]*>', re.I)
SCRIPT_RE = re.compile(r'<script\\b[^>]*\\bsrc=["\\']([^"\\']+)["\\'][^>]*>', re.I)
ALT_RE = re.compile(r'\\balt=["\\']([^"\\']*)["\\']', re.I)
REMOTE_SCHEMES = ("http://", "https://", "data:", "blob:")
INTERACTIVE_PATTERNS = (
    re.compile(r'class=["\\'][^"\\']*interactive-lab', re.I),
    re.compile(r'<(?:input|button|select|textarea|canvas)\\b', re.I),
    re.compile(r'\\bdata-[a-z0-9_-]+(?:=|\\s|>)', re.I),
)
CORE_MARKERS = ("Retrieval Practice", "完成证据", "Primary Sources")


def local_target(page: Path, raw: str):
    raw = raw.strip()
    if not raw or raw.startswith("#") or raw.startswith(REMOTE_SCHEMES):
        return None
    raw = raw.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw:
        return None
    return (page.parent / unquote(raw)).resolve()


def main():
    errors = []
    htmls = sorted(LESSONS.glob("*/*.html"))
    visual_pages = 0
    interactive_pages = 0
    teaching_surface_pages = 0
    visual_refs = 0
    interactive_script_refs = 0

    if len(htmls) != EXPECTED_LESSON_HTML_COUNT:
        errors.append(
            f"expected {EXPECTED_LESSON_HTML_COUNT} lesson HTML files, found {len(htmls)}"
        )

    root_resolved = ROOT.resolve()

    for page in htmls:
        rel = page.relative_to(ROOT)
        text = page.read_text(encoding="utf-8")

        for marker in CORE_MARKERS:
            if marker not in text:
                errors.append(f"{rel}: missing {marker}")
        if "</body>" not in text or "</html>" not in text:
            errors.append(f"{rel}: incomplete HTML document")

        local_imgs = []
        for match in IMG_RE.finditer(text):
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

            local_imgs.append((match, src))
            visual_refs += 1

            alt_match = ALT_RE.search(match.group(0))
            if not alt_match or not alt_match.group(1).strip():
                errors.append(f"{rel}: teaching image missing non-empty alt -> {src}")

        if local_imgs:
            visual_pages += 1
            if "<figcaption" not in text.lower():
                errors.append(f"{rel}: local teaching image present but no figcaption")

        interactive = any(pattern.search(text) for pattern in INTERACTIVE_PATTERNS)
        if interactive:
            interactive_pages += 1
            for match in SCRIPT_RE.finditer(text):
                src = match.group(1)
                target = local_target(page, src)
                if target is None:
                    continue
                try:
                    target.relative_to(root_resolved)
                except ValueError:
                    errors.append(f"{rel}: script src escapes repo -> {src}")
                    continue
                if not target.exists():
                    errors.append(f"{rel}: broken script src -> {src}")
                else:
                    interactive_script_refs += 1

        if local_imgs or interactive:
            teaching_surface_pages += 1
        else:
            errors.append(f"{rel}: no local visual or interactive teaching surface")

    print("VISUAL / COMPREHENSION CLOSURE AUDIT")
    print(f"lesson_html={len(htmls)}")
    print(f"visual_pages={visual_pages}")
    print(f"interactive_pages={interactive_pages}")
    print(f"pages_with_teaching_surface={teaching_surface_pages}")
    print(f"local_visual_refs={visual_refs}")
    print(f"local_interactive_script_refs={interactive_script_refs}")

    if errors:
        print(f"errors={len(errors)}")
        for error in errors:
            print("- " + error)
        print("VISUAL / COMPREHENSION CLOSURE: BLOCKED")
        raise SystemExit(2)

    print("errors=0")
    print("VISUAL / COMPREHENSION CLOSURE: PASS")


if __name__ == "__main__":
    main()
