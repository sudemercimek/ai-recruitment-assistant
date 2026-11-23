import json
from pathlib import Path

from app.models.candidate import CandidateProfile


def load_candidates(file_path: str) -> list[CandidateProfile]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    candidates = [
        CandidateProfile.model_validate(candidate)
        for candidate in data
    ]

    return candidates