# Milestones class

from __future__ import annotations

from datetime import datetime
from typing import Any

class Milestone:
    def __init__(
            self,
            milestoneId: int,
            name: str,
            createAt: datetime,
            deadline: datetime,

    ):
        