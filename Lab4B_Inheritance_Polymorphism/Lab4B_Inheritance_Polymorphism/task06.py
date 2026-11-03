"""
Task 6 — The export that refused the cloud

Answers:
6.1 export_report needs a target that provides write(bytes) and returns an
    integer. It does not need a particular file class.
6.2 Writable Protocol describes that small interface for static typing.
6.3 BytesIO, S3Upload and FakeUpload work without a shared parent class.
6.4 mypy can detect a statically known object without write() before runtime.
    The invalid example is kept as a comment so this file's checks stay clean.
"""

import io
from typing import Protocol


class Writable(Protocol):
    def write(self, data: bytes) -> int:
        ...


def export_report(rows: list[tuple[object, ...]], target: Writable) -> None:
    for row in rows:
        line = (",".join(map(str, row)) + "\n").encode()
        target.write(line)


class S3Upload:
    def __init__(self, bucket: str, key: str) -> None:
        self.bucket = bucket
        self.key = key
        self.parts: list[bytes] = []

    def write(self, data: bytes) -> int:
        self.parts.append(data)
        return len(data)


class FakeUpload:
    def __init__(self) -> None:
        self.data = bytearray()

    def write(self, data: bytes) -> int:
        self.data.extend(data)
        return len(data)


def test_export_to_bytesio():
    target = io.BytesIO()
    export_report([("Ali", 100), ("Vali", 200)], target)
    assert target.getvalue() == b"Ali,100\nVali,200\n"


def test_export_to_s3_upload():
    target = S3Upload("reports", "daily.csv")
    export_report([("Ali", 100)], target)
    assert b"".join(target.parts) == b"Ali,100\n"


def test_export_to_fake_upload():
    target = FakeUpload()
    export_report([("Vali", 200)], target)
    assert bytes(target.data) == b"Vali,200\n"


# mypy example (uncomment to see the static type error):
# export_report([("Ali", 100)], object())
