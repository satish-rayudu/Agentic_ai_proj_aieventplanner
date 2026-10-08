from typing import TypedDict


class EventState(TypedDict, total=False):
    event_request: str
    requirements: str
    budget_plan: str
    schedule_plan: str
    final_plan: str