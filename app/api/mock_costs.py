from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.mock_cost_service import create_mock_costs_from_transactions


router = APIRouter(prefix="/tools/mock-costs", tags=["mock-costs"])


class MockCostRequest(BaseModel):
    effective_date: date | None = None
    cost_ratio: Decimal = Field(default=Decimal("0.45"), gt=0, lt=1)


class MockCostResponse(BaseModel):
    import_id: int
    row_count: int
    effective_date: str
    cost_ratio: float


@router.post("/from-transactions", response_model=MockCostResponse)
async def mock_costs_from_transactions(
    payload: MockCostRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MockCostResponse:
    effective_date = payload.effective_date or datetime.utcnow().date()
    cost_import = await create_mock_costs_from_transactions(
        db=db,
        effective_date=effective_date,
        cost_ratio=payload.cost_ratio,
    )
    return MockCostResponse(
        import_id=cost_import.id,
        row_count=cost_import.row_count,
        effective_date=cost_import.effective_date.isoformat(),
        cost_ratio=float(payload.cost_ratio),
    )

