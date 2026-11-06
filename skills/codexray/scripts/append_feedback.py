#!/usr/bin/env python3
"""Private CodeXRay feedback storage; Python standard library only."""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sys
import tempfile
import time


SKILL_DIR = Path(__file__).resolve().parent.parent


def state_paths():
    override = os.environ.get("CODEXRAY_HOME", "").strip()
    root = Path(os.path.expandvars(override)).expanduser() if override else Path.home() / ".codexray"
    root = root.resolve()
    if root == SKILL_DIR or SKILL_DIR in root.parents:
        raise ValueError("CODEXRAY_HOME must be outside the installed skill directory")
    return {
        "state_dir": str(root),
        "reference": str(root / "reference.json"),
        "personalized_prompt": str(root / "runtime-prompt-personalized.md"),
    }


def load_document(path):
    if not path.exists():
        return {"schema_version": 1, "feedback": []}
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(doc, dict) or not isinstance(doc.get("feedback"), list):
        raise ValueError("reference.json must be an object with a feedback array; file left unchanged")
    return doc


def clean_text(value, field):
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(field + " must be a string")
    return value.strip()


def text_list(value, field):
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        raise ValueError(field + " must be a string or array of strings")
    return [item for item in (clean_text(v, field) for v in value) if item]


def make_record(payload):
    if not isinstance(payload, dict):
        raise ValueError("feedback must be a JSON object")
    record = {
        "user_query": clean_text(payload.get("user_query"), "user_query"),
        "positive": text_list(payload.get("positive"), "positive"),
        "negative": text_list(payload.get("negative"), "negative"),
        "preference": clean_text(payload.get("preference"), "preference"),
        "scope": clean_text(payload.get("scope"), "scope"),
    }
    if not record["user_query"]:
        raise ValueError("user_query must identify the evaluated task")
    if not any(record[k] for k in ("positive", "negative", "preference")):
        raise ValueError("explicit feedback or a stated preference is required")
    return record


def atomic_write(path, raw):
    fd, temporary = tempfile.mkstemp(prefix=".codexray-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def profile_lock(root):
    root.mkdir(parents=True, exist_ok=True)
    lock = root / ".write.lock"
    deadline = time.monotonic() + 5
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise ValueError("profile is locked; retry later (after a crashed writer, inspect " + str(lock) + ")")
            time.sleep(0.05)
    try:
        yield
    finally:
        lock.unlink()


def encode_document(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--paths", action="store_true", help="show profile paths without writing")
    modes.add_argument("--init", action="store_true", help="initialize empty feedback storage")
    modes.add_argument("--list", action="store_true", help="show records without writing")
    modes.add_argument("--save-prompt", metavar="FILE", help="atomically save a synthesized UTF-8 prompt")
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--file", help="UTF-8 JSON file containing one feedback record")
    sources.add_argument("--json", help="one feedback record as JSON")
    parser.add_argument("--query")
    parser.add_argument("--positive", action="append")
    parser.add_argument("--negative", action="append")
    parser.add_argument("--preference")
    parser.add_argument("--scope")
    parser.add_argument("--dry-run", action="store_true", help="validate an append without writing")
    args = parser.parse_args(argv)
    fields = (args.query, args.positive, args.negative, args.preference, args.scope)
    has_source = args.file is not None or args.json is not None
    if has_source and any(v is not None for v in fields):
        parser.error("use either --file/--json or feedback fields, not both")
    if (args.paths or args.init or args.list or args.save_prompt) and (has_source or any(v is not None for v in fields) or args.dry_run):
        parser.error("profile modes cannot be combined with feedback fields or --dry-run")

    paths = state_paths()
    root = Path(paths["state_dir"])
    reference = Path(paths["reference"])
    if args.paths:
        print(json.dumps(paths, ensure_ascii=False, indent=2))
        return 0
    if args.list:
        print(json.dumps(load_document(reference)["feedback"], ensure_ascii=False, indent=2))
        return 0
    if args.init:
        with profile_lock(root):
            doc = load_document(reference)
            if not reference.exists():
                atomic_write(reference, encode_document(doc))
        print(json.dumps(dict(paths, feedback_records=len(doc["feedback"])), ensure_ascii=False, indent=2))
        return 0
    if args.save_prompt:
        candidate = Path(args.save_prompt).read_bytes().decode("utf-8-sig")
        if not candidate.strip():
            raise ValueError("candidate prompt is empty; saved prompt left unchanged")
        raw = candidate.encode("utf-8")
        prompt = Path(paths["personalized_prompt"])
        with profile_lock(root):
            if not load_document(reference)["feedback"]:
                raise ValueError("cannot synthesize preferences without feedback")
            unchanged = prompt.exists() and prompt.read_bytes() == raw
            if not unchanged:
                atomic_write(prompt, raw)
            if prompt.read_bytes() != raw:
                raise OSError("saved prompt verification failed")
        print(json.dumps({"status": "unchanged" if unchanged else "saved", "path": str(prompt)}, ensure_ascii=False))
        return 0

    if args.file is not None:
        payload = json.loads(Path(args.file).read_text(encoding="utf-8-sig"))
    elif args.json is not None:
        payload = json.loads(args.json)
    else:
        payload = dict(zip(("user_query", "positive", "negative", "preference", "scope"), fields))
    record = make_record(payload)
    if args.dry_run:
        doc = load_document(reference)
        print(json.dumps({"status": "dry-run", "path": str(reference), "record": record, "duplicate": record in doc["feedback"]}, ensure_ascii=False, indent=2))
        return 0
    with profile_lock(root):
        doc = load_document(reference)
        duplicate = record in doc["feedback"]
        if not duplicate:
            doc["feedback"].append(record)
            atomic_write(reference, encode_document(doc))
        if record not in load_document(reference)["feedback"]:
            raise OSError("saved feedback verification failed")
    print(json.dumps({"status": "duplicate" if duplicate else "appended", "path": str(reference), "feedback_records": len(doc["feedback"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        sys.exit(2)
