from datetime import date

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel


class Publication_params(BaseModel):
    search: str | None = None
    publication_type_id: int | None = None
    author_id: int | None = None
    source_rating_type_id: int | None = None
    department_id: int | None = None
    from_date: date = date(1960, 1, 1)
    to_date: date = date.today()
    page: int = 0
    limit: int = 20

