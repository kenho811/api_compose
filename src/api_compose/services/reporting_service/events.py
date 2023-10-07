from api_compose.core.events.base import BaseEvent, EventType, BaseData


# Registration
class ReportingEvent(BaseEvent):
    event: EventType = EventType.Reporting
    data: BaseData = BaseData()
