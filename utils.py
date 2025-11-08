"""
Utility functions for the Neuro Assessment application.
"""

import re
from typing import Dict, List, Any
from datetime import datetime
from constants import MEMORY_WORD_LIST


def normalize_text(text: str) -> List[str]:
    """Normalize text input: split, strip, uppercase, remove punctuation."""
    if not text:
        return []
    # Split by whitespace and commas
    tokens = re.split(r'[\s,]+', text.strip())
    # Remove punctuation and convert to uppercase
    normalized = [re.sub(r'[^\w]', '', token).upper() for token in tokens if token]
    return normalized


def score_recall(recalled: List[str], word_list: List[str]) -> int:
    """Score recalled words against word list (case-insensitive, unique matches)."""
    recalled_set = set(recalled)
    word_set = set(word.upper() for word in word_list)
    return len(recalled_set & word_set)


def initialize_assessment_state() -> Dict[str, Any]:
    """Initialize the assessment state dictionary with default values."""
    return {
        "meta": {
            "app_version": "1.0.0",
            "start_timestamp": None,
            "end_timestamp": None,
            "duration_seconds": None,
            "assessor_notes": ""
        },
        "participant": {
            "full_name": "",
            "participant_id": ""
        },
        "symptoms": {},
        "cognitive": {
            "immediate_memory": {
                "word_list": MEMORY_WORD_LIST.copy(),
                "trials": [],
                "total_score": 0,
                "max_score": 15
            },
            "delayed_recall": {
                "recalled": [],
                "score": 0,
                "max_score": 5
            }
        },
        "balance": {
            "status": "placeholder"
        },
        "eye_tracking": {
            "status": "placeholder"
        }
    }

