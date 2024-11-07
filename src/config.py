"""Configuration classes for the Neologismen experiment."""

from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class ExperimentConfig:
    """Configuration settings for the experiment."""
    window_size: Tuple[int, int] = (1024, 768)
    max_attempts: int = 5
    instruction_sections: List[str] = field(default_factory=lambda: [
        'Welcome', 'Task Introduction', 'Input Instructions',
        'Definition Info', 'Controls', 'Exit Info'
    ])
    definition_display_time: float = 3.0
    blink_interval: float = 0.5

@dataclass
class ParticipantInfo:
    """Data class to store participant information."""
    name: str
    age: str
    gender: str
    session_name: str
    word_count: str
    language: str
