from __future__ import annotations

import json

import pytest

from scripts.run_experiments import completed_example_ids


def test_completed_example_ids_accepts_interrupted_valid_jsonl(tmp_path):
    output = tmp_path / "predictions.jsonl"
    output.write_text(
        "\n".join(
            [
                json.dumps({"example_id": "study-1::view-a"}),
                json.dumps({"study_id": "legacy-study-2"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    assert completed_example_ids(output) == {"study-1::view-a", "legacy-study-2"}
    assert completed_example_ids(tmp_path / "missing.jsonl") == set()


@pytest.mark.parametrize(
    "contents, message",
    [
        ('{"example_id":"one"}\nnot-json\n', "malformed JSON"),
        ('{"example_id":"one"}\n{"example_id":"one"}\n', "duplicate example ID"),
        ('{"final_report":"No edema."}\n', "has no example ID"),
    ],
)
def test_completed_example_ids_rejects_unsafe_resume_files(tmp_path, contents, message):
    output = tmp_path / "predictions.jsonl"
    output.write_text(contents, encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        completed_example_ids(output)
