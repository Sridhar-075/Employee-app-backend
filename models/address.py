from typing import Any, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from models.entity import Entity
from database import Base

from datetime import datetime

if TYPE_CHECKING:
    from models.employee import Employee

def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class Address(Entity):
    __tablename__ = "address"
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    line1 : Mapped[str] = mapped_column(String(100), nullable=False)
    city:  Mapped[str] = mapped_column(String(100), nullable=False)
    postalcode: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    employee: Mapped["Employee"] = relationship("Employee", back_populates="addresses")

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "line1": self.id,
            "city": self.city,
            "postalcode": self.postalcode,
            "country":self.country,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }