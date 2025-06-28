from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class BuildingAmenity(Base):
    __tablename__ = "building_amenity"

    building_id: Mapped[int] = mapped_column(Integer,
        ForeignKey("building.id"), primary_key=True
    )
    amenity_id: Mapped[int] = mapped_column(Integer,
        ForeignKey("amenity.id"), primary_key=True
    )


class BuildingHeating(Base):
    __tablename__ = "building_heating"

    building_id: Mapped[int] = mapped_column(Integer,
        ForeignKey("building.id"), primary_key=True
    )
    heating_id: Mapped[int] = mapped_column(Integer,
        ForeignKey("heating.id"), primary_key=True
    )

class Amenity(Base):
    __tablename__ = "amenity"

    id:   Mapped[int]  = mapped_column(Integer, primary_key=True)
    name: Mapped[str]  = mapped_column(String, nullable=False, unique=True)

    buildings: Mapped[list["Building"]] = relationship(
        secondary="building_amenity", back_populates="amenities"
    )

class Heating(Base):
    __tablename__ = "heating"

    id:   Mapped[int]  = mapped_column(Integer, primary_key=True)
    name: Mapped[str]  = mapped_column(String, nullable=False, unique=True)

    buildings: Mapped[list["Building"]] = relationship(
        secondary="building_heating", back_populates="heatings"
    )


class EstateType(Base):
    __tablename__ = "estate_type"

    id:   Mapped[int]  = mapped_column(Integer, primary_key=True)
    name: Mapped[str]  = mapped_column(String, nullable=False, unique=True)

    buildings: Mapped[list["Building"]] = relationship(back_populates="estate_type")


class Offer(Base):
    __tablename__ = "offer"

    id:   Mapped[int]  = mapped_column(Integer, primary_key=True)
    name: Mapped[str]  = mapped_column(String, nullable=False, unique=True)

    buildings: Mapped[list["Building"]] = relationship(back_populates="offer")