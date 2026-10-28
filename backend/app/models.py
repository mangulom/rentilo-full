from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Person(Base):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(40), default="")
    role: Mapped[str] = mapped_column(String(24), default="tenant")


class Property(Base):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(180), index=True)
    address: Mapped[str] = mapped_column(String(240))
    city: Mapped[str] = mapped_column(String(100), default="Lima")
    kind: Mapped[str] = mapped_column(String(40), default="Departamento")
    bedrooms: Mapped[int] = mapped_column(Integer, default=1)
    monthly_rent: Mapped[float] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(24), default="Disponible", index=True)
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("people.id"), nullable=True)
    owner: Mapped[Person | None] = relationship()


class Lease(Base):
    __tablename__ = "leases"
    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("people.id"), index=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date, index=True)
    monthly_rent: Mapped[float] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(24), default="Activo", index=True)
    property: Mapped[Property] = relationship()
    tenant: Mapped[Person] = relationship()


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(24), default="Abierto", index=True)
    priority: Mapped[str] = mapped_column(String(24), default="Normal")
