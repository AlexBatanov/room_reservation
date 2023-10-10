# app/crud/reservation.py

# Новый импорт для аннотации параметров.
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from app.crud.base import CRUDBase
from app.models.reservation import Reservation


# Новый класс должен быть унаследован от CRUDBase.
class CRUDReservation(CRUDBase):

    async def get_reservations_at_the_same_time(
        self,
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: Optional[int] = None,
        session: AsyncSession,
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )

        if reservation_id is not None:
            select_stmt = select_stmt.where(
                # id искомых объектов не равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations


# Создаём объекта класса CRUDReservation.
reservation_crud = CRUDReservation(Reservation)
