import csv

import pytest

from load_scores import load_scores


def _write_csv(tmp_path, rows):
    path = tmp_path / "scores.csv"
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "score"])
        writer.writerows(rows)
    return path


def test_multiple_valid_rows_keep_their_order_and_quoted_names(tmp_path):
    path = _write_csv(
        tmp_path,
        [
            ("김하나", "88"),
            ("최,네번", "77"),
            ("이두리", "91"),
        ],
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("김하나", 88),
        ("최,네번", 77),
        ("이두리", 91),
    ]
    assert skipped == []


def test_header_only_file_returns_no_records(tmp_path):
    path = _write_csv(tmp_path, [])

    assert load_scores(path) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    "row",
    [
        ("이름만",),
        ("이름", "80", "메모"),
        ("", "90"),
        ("이름", ""),
        ("이름", "결석"),
        ("이름", "8 0"),
        ("이름", "-1"),
        ("이름", "101"),
    ],
)
def test_invalid_rows_are_excluded_and_reported(tmp_path, row):
    path = _write_csv(tmp_path, [row])

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][0] == 2


@pytest.mark.parametrize(
    ("score", "is_valid"),
    [
        (0, True),
        (100, True),
        (-1, False),
        (101, False),
    ],
)
def test_score_boundaries_are_not_corrected(tmp_path, score, is_valid):
    path = _write_csv(tmp_path, [("경계", str(score))])

    kept, skipped = load_scores(path)

    assert bool(kept) is is_valid
    assert bool(skipped) is (not is_valid)
    if is_valid:
        assert kept[0] == ("경계", score)


def test_blank_line_and_duplicate_name_do_not_hide_later_line_number(tmp_path):
    path = tmp_path / "line-numbers.csv"
    path.write_text(
        "name,score\n같은이름,70\n같은이름,80\n\n마지막,101\n",
        encoding="utf-8",
    )

    _, skipped = load_scores(path)

    assert len(skipped) == 1
    assert skipped[0][0] == 5
