from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Lease, MaintenanceRequest, Person, Property

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Rentilo API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["*"], allow_headers=["*"], allow_credentials=False)


def get_db():
    with SessionLocal() as db:
        yield db


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/properties")
def properties(q: str = "", status: str = "", db: Session = Depends(get_db)):
    stmt = select(Property).order_by(Property.id.desc())
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Property.title.ilike(like), Property.address.ilike(like), Property.code.ilike(like)))
    if status:
        stmt = stmt.where(Property.status == status)
    return [{"id": row.id, "code": row.code, "title": row.title, "address": row.address, "city": row.city, "kind": row.kind, "bedrooms": row.bedrooms, "monthly_rent": float(row.monthly_rent), "status": row.status, "owner_id": row.owner_id} for row in db.scalars(stmt).all()]


@app.post("/api/properties", status_code=201)
def create_property(payload: dict, db: Session = Depends(get_db)):
    required = ("code", "title", "address", "monthly_rent")
    if any(not payload.get(key) for key in required):
        raise HTTPException(422, "Completa código, nombre, dirección y alquiler mensual")
    item = Property(**{key: value for key, value in payload.items() if key in {"code", "title", "address", "city", "kind", "bedrooms", "monthly_rent", "status", "owner_id"}})
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "code": item.code, "title": item.title, "address": item.address, "city": item.city, "kind": item.kind, "bedrooms": item.bedrooms, "monthly_rent": float(item.monthly_rent), "status": item.status, "owner_id": item.owner_id}


@app.get("/api/people")
def people(q: str = "", role: str = "", db: Session = Depends(get_db)):
    stmt = select(Person).order_by(Person.name)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Person.name.ilike(like), Person.email.ilike(like), Person.phone.ilike(like)))
    if role:
        stmt = stmt.where(Person.role == role)
    return [{"id": row.id, "name": row.name, "email": row.email, "phone": row.phone, "role": row.role} for row in db.scalars(stmt).all()]


@app.get("/api/leases")
def leases(db: Session = Depends(get_db)):
    rows = db.scalars(select(Lease).order_by(Lease.end_date)).all()
    return [{"id": row.id, "property_id": row.property_id, "property": row.property.title, "tenant_id": row.tenant_id, "tenant": row.tenant.name, "start_date": row.start_date, "end_date": row.end_date, "monthly_rent": float(row.monthly_rent), "status": row.status} for row in rows]


@app.get("/api/maintenance")
def maintenance(status: str = Query(default=""), db: Session = Depends(get_db)):
    stmt = select(MaintenanceRequest).order_by(MaintenanceRequest.id.desc())
    if status:
        stmt = stmt.where(MaintenanceRequest.status == status)
    return [{"id": row.id, "property_id": row.property_id, "title": row.title, "description": row.description, "status": row.status, "priority": row.priority} for row in db.scalars(stmt).all()]
