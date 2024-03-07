from datetime import date
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel


class Rid_params(BaseModel):
    search: str | None = None
    author_id: int | None = None
    from_date: date = date(1960, 1, 1)
    to_date: date = date.today()
    page: int = 0
    limit: int = 20

