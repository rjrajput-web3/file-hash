# file-hash

Print cryptographic hashes of files. Stdlib-only Python CLI — no
dependencies, no install step, runs anywhere Python 3 runs.

Use it to verify a download against a published checksum, or to confirm
two files are byte-for-byte identical without opening them.

## Usage

```sh
python file_hash.py FILE [FILE ...] [-a ALGORITHM] [--json]
cat archive.zip | python file_hash.py - [-a sha256]
```

Algorithms: `md5`, `sha1`, `sha256` (default), `sha512`.

## Example

```sh
$ python file_hash.py sample.txt
c03905fcdab297513a620ec81ed46ca44ddb62d41cbbd83eb4a5a3592be26a69  sample.txt

$ python file_hash.py -a md5 sample.txt
37c4b87edffc5d198ff5a185cee7ee09  sample.txt

$ printf 'hello\n' | python file_hash.py -
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03  -

$ python file_hash.py --json sample.txt
{
  "sample.txt": "c03905fcdab297513a620ec81ed46ca44ddb62d41cbbd83eb4a5a3592be26a69"
}
```

## Exit codes

- `0` — every file hashed cleanly.
- `2` — any error: missing file, a directory passed as a file, an
  unreadable file, or an unknown algorithm. The files that did hash are
  still printed; the error is reported on stderr.

## How it works

Files are read in 64 KB chunks, so hashing a multi-gigabyte file uses
almost no memory. `sample.txt` contains one line,
`The quick brown fox jumps over the lazy dog`, so you can check the
tool against your system's own `sha256sum` / `md5sum`.
