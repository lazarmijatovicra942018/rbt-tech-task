from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class State(Base):
    __tablename__ = 'state'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    cities: Mapped[list["City"]] = relationship(back_populates='state')

class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey('state.id'))

    state: Mapped["State"] = relationship(back_populates='cities')
    parts: Mapped[list["CityPart"]] = relationship(
        back_populates='city'
    )

class CityPart(Base):
    __tablename__ = 'city_part'
    __table_args__ = (
        UniqueConstraint('name', 'city_id', name='city_parts_name_city_id_key'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('city.id'))

    city: Mapped["City"] = relationship(back_populates='parts')
    buildings: Mapped[list["Building"]] = relationship(back_populates='city_part')