from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass(frozen=True)
class TaskType:
    name: str
    color: str = "#cccccc"

@dataclass
class BaseTask:
    name: str
    task_type: TaskType
    priority: int = 3

    def to_dict(self):
        d = asdict(self)
        d['task_type'] = self.task_type.name  # Convert TaskType to string
        return d
@dataclass
class Task(BaseTask):
    est: int = 30
    complete: bool = False
    chain: Optional[str] = None

@dataclass
class SavedTask(BaseTask):
    default_est: int = 30
    note: Optional[str] = None

