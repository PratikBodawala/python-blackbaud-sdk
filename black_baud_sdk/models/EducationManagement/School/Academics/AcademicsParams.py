from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Assignment:
    id: Optional[int]  # Can't fucking believe it that it can be null
    date: Optional[str]
    description: Optional[str]
    discussion: Optional[bool]
    due_date: Optional[str]
    enrolled: Optional[int]
    graded_count: Optional[int]
    index_id: Optional[int]
    major: Optional[bool]
    name: Optional[str]
    publish_on_assigned: Optional[bool]
    published: Optional[bool]
    rank: Optional[int]
    status: Optional[int]
    type: Optional[str]
    type_id: Optional[int]


@dataclass
class AcademicsAssignmentsBySectionParams:
    section_id: int
    types: Optional[str] = None
    status: Optional[str] = None
    persona_id: Optional[int] = None
    filter: Optional[str] = None
    search: Optional[str] = None


@dataclass
class AcademicsAssignmentsBySectionResponse:
    count: int
    value: List[Assignment]
    next_link: Optional[str] = None
