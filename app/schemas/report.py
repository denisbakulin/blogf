from base.schemas import BaseSchema

class CreateReport(BaseSchema):
    reason: str | None = None

