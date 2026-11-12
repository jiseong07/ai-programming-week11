
import csv

import pytest

from load_scores import load_scores


def _write_scores(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "score"])
        writer.writerows(rows)
    return path


def test_real_scores_file_keeps_valid_rows_and_reports_bad_rows():
    kept, skipped = load_scores("scores.csv")

    assert kept == [
        ("김하나", 88),
        ("최,네번", 77),
        ("김하나", 91),
        ("윤보람", 64),
        ("서한별", 95),
    ]
    assert [line_no for line_no, _, _ in skipped] == [3, 4, 7, 8, 9]
    assert [reason for _, _, reason in skipped] == [
        "점수가 0~100 밖",
        "점수가 비어 있음",
        "점수가 0~100 밖",
        "점수가 정수가 아님",
        "열 개수가 2가 아님",
    ]


def test_header_only_file_returns_no_scores(tmp_path):
    path = _write_scores(tmp_path / "header.csv", [])

    assert load_scores(path) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    ("score", "expected_kept"),
    [
        (-1, []),
        (0, [("경계", 0)]),
        (1, [("경계", 1)]),
        (99, [("경계", 99)]),
        (100, [("경계", 100)]),
        (101, []),
    ],
)
def test_score_range_boundaries(tmp_path, score, expected_kept):
    path = _write_scores(tmp_path / "boundary.csv", [("경계", str(score))])

    kept, skipped = load_scores(path)

    assert kept == expected_kept
    assert bool(skipped) is (not bool(expected_kept))


def test_utf8_bom_and_duplicate_names_are_supported(tmp_path):
    path = tmp_path / "duplicates.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "score"])
        writer.writerow(["같은이름", 70])
        writer.writerow(["같은이름", 80])

    kept, skipped = load_scores(path)

    assert kept == [("같은이름", 70), ("같은이름", 80)]
    assert skipped == []
