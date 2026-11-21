#!/usr/bin/env python3
"""Print cryptographic hashes of files — stdlib only.

Usage:
    python file_hash.py FILE [FILE ...] [-a ALGORITHM] [--json]
    cat archive.zip | python file_hash.py - [-a sha256]

Algorithms: md5, sha1, sha256 (default), sha512.
Exit code 0 when every file hashes cleanly, 2 on any error
(missing file, unreadable file, unknown algorithm).
"""

import argparse
import hashlib
import json
import sys

ALGORITHMS = ("md5", "sha1", "sha256", "sha512")


def hash_stream(stream, algorithm):
    digest = hashlib.new(algorithm)
    while True:
        chunk = stream.read(65536)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def hash_path(path, algorithm):
    if path == "-":
        return hash_stream(sys.stdin.buffer, algorithm)
    with open(path, "rb") as handle:
        return hash_stream(handle, algorithm)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print cryptographic hashes of files."
    )
    parser.add_argument("files", nargs="+", metavar="FILE",
                        help="file to hash (use - for stdin)")
    parser.add_argument("-a", "--algorithm", default="sha256",
                        choices=ALGORITHMS,
                        help="hash algorithm (default: sha256)")
    parser.add_argument("--json", action="store_true",
                        help="print results as a JSON object")
    args = parser.parse_args(argv)

    results = {}
    failed = False
    for path in args.files:
        try:
            results[path] = hash_path(path, args.algorithm)
        except FileNotFoundError:
            print(f"file-hash: {path}: No such file", file=sys.stderr)
            failed = True
        except IsADirectoryError:
            print(f"file-hash: {path}: Is a directory", file=sys.stderr)
            failed = True
        except PermissionError:
            print(f"file-hash: {path}: Permission denied", file=sys.stderr)
            failed = True
        except OSError as exc:
            print(f"file-hash: {path}: {exc.strerror or exc}", file=sys.stderr)
            failed = True

    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for path in args.files:
            if path in results:
                print(f"{results[path]}  {path}")

    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
