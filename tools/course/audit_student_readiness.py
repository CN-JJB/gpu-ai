#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "lessons"
EXPERIMENTS = ROOT / "labs" / "experiments"
CHALLENGES = ROOT / "labs" / "challenges"
CURRICULUM = ROOT / "curriculum"

EXPECTED_SLICE_COUNT = 49
EXPECTED_LESSON_HTML_COUNT = 62
EXPECTED_EXPERIMENT_COUNT = 93
EXPECTED_CHALLENGE_COUNT = 12

FOUNDATIONS = {
    "00-how-to-use-course.md",
    "01-shell-paths-processes.md",
    "02-python-json-hash.md",
    "03-math-units-estimation.md",
    "04-git-source-reading.md",
    "05-safety-experiment-discipline.md",
}

REAL_RESULT_ARTIFACTS = {
    "RESULT-TEMPLATE.md",
    "QUALITY-RESULT-TEMPLATE.md",
    "CAPSTONE-CARD.md",
    "INCIDENT-TEMPLATE.md",
    "DESIGN-REPORT-TEMPLATE.md",
    "CAPSTONE-REPORT-TEMPLATE.md",
}

HTML_LINK_RE = re.compile(r'href=[\"\']([^\"\']+)[\"\']', re.I)
MD_LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
REMOTE_SCHEMES = (
    "http://",
    "https://",
    "mailto:",
    "data:",
    "javascript:",
)


def fail(errors, message):
    errors.append(message)


def top_level_numbered_dirs(root):
    return sorted(
        p for p in root.iterdir()
        if p.is_dir() and re.match(r"^\d{2}-", p.name)
    )


def validate_lesson_structure(errors):
    slices = top_level_numbered_dirs(LESSONS)
    if len(slices) != EXPECTED_SLICE_COUNT:
        fail(errors, f"expected {EXPECTED_SLICE_COUNT} lesson slices, found {len(slices)}")

    numbers = []
    htmls = []
    for folder in slices:
        numbers.append(int(folder.name[:2]))
        htmls.extend(sorted(folder.glob("*.html")))

    if numbers != list(range(1, EXPECTED_SLICE_COUNT + 1)):
        fail(errors, f"lesson slice numbering is not 01..49: {numbers}")

    if len(htmls) != EXPECTED_LESSON_HTML_COUNT:
        fail(
            errors,
            f"expected {EXPECTED_LESSON_HTML_COUNT} lesson HTML files, found {len(htmls)}",
        )

    for path in htmls:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if "Retrieval Practice" not in text:
            fail(errors, f"{rel}: missing Retrieval Practice")
        if "完成证据" not in text:
            fail(errors, f"{rel}: missing 完成证据")
        if "Primary Sources" not in text:
            fail(errors, f"{rel}: missing Primary Sources / Reference")
        if "</body>" not in text or "</html>" not in text:
            fail(errors, f"{rel}: incomplete HTML document")
        if path.stat().st_size < 1500:
            fail(errors, f"{rel}: suspiciously small lesson ({path.stat().st_size} bytes)")


def validate_experiments(errors):
    experiments = top_level_numbered_dirs(EXPERIMENTS)
    if len(experiments) != EXPECTED_EXPERIMENT_COUNT:
        fail(errors, f"expected {EXPECTED_EXPERIMENT_COUNT} experiments, found {len(experiments)}")

    numbers = [int(p.name[:2]) for p in experiments]
    if numbers != list(range(1, EXPECTED_EXPERIMENT_COUNT + 1)):
        fail(errors, f"experiment numbering is not 01..93: {numbers}")

    for folder in experiments:
        if not (folder / "README.md").is_file():
            fail(errors, f"{folder.relative_to(ROOT)}: missing README.md")
        if not (folder / "EXPECTED.md").is_file():
            fail(errors, f"{folder.relative_to(ROOT)}: missing EXPECTED.md")

        if "-real-" in folder.name or folder.name.startswith("03-real") or folder.name.startswith("07-real"):
            present = {p.name for p in folder.iterdir() if p.is_file()}
            if not (present & REAL_RESULT_ARTIFACTS):
                fail(
                    errors,
                    f"{folder.relative_to(ROOT)}: real experiment lacks a recognized result/report template",
                )


def validate_challenges(errors):
    challenge_dirs = top_level_numbered_dirs(CHALLENGES)
    if len(challenge_dirs) != EXPECTED_CHALLENGE_COUNT:
        fail(
            errors,
            f"expected {EXPECTED_CHALLENGE_COUNT} challenge labs, found {len(challenge_dirs)}",
        )

    numbers = [int(p.name[:2]) for p in challenge_dirs]
    if numbers != list(range(1, EXPECTED_CHALLENGE_COUNT + 1)):
        fail(errors, f"challenge numbering is not 01..12: {numbers}")

    if not (CHALLENGES / "CHALLENGE-CARD.md").is_file():
        fail(errors, "labs/challenges: missing CHALLENGE-CARD.md")

    for folder in challenge_dirs:
        if not (folder / "README.md").is_file():
            fail(errors, f"{folder.relative_to(ROOT)}: missing README.md")
        if not (folder / "EXPECTED.md").is_file():
            fail(errors, f"{folder.relative_to(ROOT)}: missing EXPECTED.md")
        readme = (folder / "README.md").read_text(encoding="utf-8")
        for marker in ("Retrieval Practice", "完成证据"):
            if marker not in readme:
                fail(errors, f"{folder.relative_to(ROOT)}/README.md: missing {marker}")


def validate_curriculum(errors):
    if not (CURRICULUM / "README.md").is_file():
        fail(errors, "curriculum/README.md missing")

    foundations_dir = CURRICULUM / "foundations"
    present = {p.name for p in foundations_dir.glob("*.md")}
    missing = FOUNDATIONS - present
    if missing:
        fail(errors, f"missing foundation files: {sorted(missing)}")


def local_link_targets(path, text):
    links = []
    if path.suffix.lower() == ".html":
        links.extend(HTML_LINK_RE.findall(text))
    if path.suffix.lower() == ".md":
        links.extend(MD_LINK_RE.findall(text))

    for raw in links:
        raw = raw.strip()
        if not raw or raw.startswith("#") or raw.startswith(REMOTE_SCHEMES):
            continue
        raw = raw.split("#", 1)[0].split("?", 1)[0].strip()
        if not raw:
            continue
        yield unquote(raw)


def validate_local_links(errors):
    roots = [
        LESSONS,
        CURRICULUM,
        CHALLENGES,
        EXPERIMENTS,
    ]
    for base in roots:
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".html"}:
                continue
            text = path.read_text(encoding="utf-8")
            for target in local_link_targets(path, text):
                target_path = (path.parent / target).resolve()
                try:
                    target_path.relative_to(ROOT.resolve())
                except ValueError:
                    fail(
                        errors,
                        f"{path.relative_to(ROOT)}: local link escapes repo: {target}",
                    )
                    continue
                if not target_path.exists():
                    fail(
                        errors,
                        f"{path.relative_to(ROOT)}: broken local link -> {target}",
                    )


def main():
    errors = []
    validate_lesson_structure(errors)
    validate_experiments(errors)
    validate_challenges(errors)
    validate_curriculum(errors)
    validate_local_links(errors)

    print("COURSE READINESS AUDIT")
    print(f"lesson_slices={len(top_level_numbered_dirs(LESSONS))}")
    print(f"lesson_html={len(list(LESSONS.glob('*/*.html')))}")
    print(f"experiments={len(top_level_numbered_dirs(EXPERIMENTS))}")
    print(f"challenges={len(top_level_numbered_dirs(CHALLENGES))}")
    print(f"foundations={len(list((CURRICULUM / 'foundations').glob('*.md')))}")

    if errors:
        print(f"errors={len(errors)}")
        for error in errors:
            print("- " + error)
        print("COURSE READINESS: BLOCKED")
        raise SystemExit(2)

    print("errors=0")
    print("COURSE READINESS: PASS")


if __name__ == "__main__":
    main()
