import csv

import pytest

from load_scores import load_scores


def _write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "score"])
        writer.writerows(rows)
    return path


def test_scores_csv_keeps_valid_rows_and_records_skipped_rows():
    kept, skipped = load_scores("scores.csv")

    assert kept == [
        ("김하나", 88),
        ("최,네번", 77),
        ("김하나", 91),
        ("윤보람", 64),
        ("서한별", 95),
    ]
    assert skipped == [
        (3, "이두리,105", "점수가 0~100 밖"),
        (4, "박세찬,", "점수가 비어 있음"),
        (7, "정오름,-5", "점수가 0~100 밖"),
        (8, "한겨울,결석", "점수가 정수가 아님"),
        (9, "장미르,72,비고없음", "열 개수가 2가 아님"),
    ]


def test_header_only_csv_returns_empty_lists():
    assert load_scores("empty.csv") == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_weird_csv_skips_invalid_rows_and_keeps_valid_rows():
    kept, skipped = load_scores("weird.csv")

    assert kept == [("한겨울", 77), ("윤보람", 88)]
    assert [reason for _, _, reason in skipped] == [
        "이름이 비어 있음",
        "점수가 비어 있음",
        "점수가 비어 있음",
        "점수가 0~100 밖",
        "점수가 0~100 밖",
        "점수가 정수가 아님",
        "점수가 정수가 아님",
    ]


@pytest.mark.parametrize(
    ("score", "is_valid"),
    [
        (-1, False),
        (0, True),
        (1, True),
        (99, True),
        (100, True),
        (101, False),
    ],
)
def test_score_boundaries(score, is_valid, tmp_path):
    path = _write_csv(tmp_path / "boundary.csv", [("테스트", str(score))])

    kept, skipped = load_scores(path)

    assert bool(kept) is is_valid
    assert bool(skipped) is (not is_valid)


def test_duplicate_names_are_kept_and_blank_lines_are_ignored(tmp_path):
    path = tmp_path / "duplicates.csv"
    path.write_text(
        "name,score\n같은이름,80\n\n같은이름,90\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == [("같은이름", 80), ("같은이름", 90)]
    assert skipped == []


def test_whitespace_is_trimmed_and_quoted_commas_are_supported(tmp_path):
    path = _write_csv(tmp_path / "quoted.csv", [("  김,쉼표  ", " 77 ")])

    kept, skipped = load_scores(path)

    assert kept == [("김,쉼표", 77)]
    assert skipped == []