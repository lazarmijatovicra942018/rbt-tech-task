from app.database import Base
from sqlalchemy import Float, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import  Mapped, mapped_column, relationship

class Building(Base):
    __tablename__ = "building"

    id:                Mapped[int]   = mapped_column(Integer, primary_key=True)
    square_footage:    Mapped[float] = mapped_column(Float)
    construction_year: Mapped[int]   = mapped_column(Integer)
    land_area:         Mapped[float] = mapped_column(Float)
    registration:      Mapped[bool]  = mapped_column(Boolean)
    rooms:             Mapped[float] = mapped_column(Float)
    bathrooms:         Mapped[int]   = mapped_column(Integer)
    parking:           Mapped[bool]  = mapped_column(Boolean)
    price:             Mapped[int]   = mapped_column(Integer)

    estate_type_id: Mapped[int] = mapped_column(Integer,
        ForeignKey("estate_type.id", ondelete="RESTRICT")
    )
    offer_id:       Mapped[int] = mapped_column(Integer,
        ForeignKey("offer.id", ondelete="RESTRICT")
    )
    city_part_id:   Mapped[int] = mapped_column(Integer,
        ForeignKey("city_part.id", ondelete="RESTRICT")
    )

    estate_type: Mapped["EstateType"] = relationship(back_populates="buildings")
    offer:       Mapped["Offer"]       = relationship(back_populates="buildings")
    city_part:   Mapped["CityPart"]    = relationship(back_populates="buildings")

    amenities: Mapped[list["Amenity"]] = relationship(
        secondary="building_amenity",
        back_populates="buildings"
    )
    heatings:  Mapped[list["Heating"]] = relationship(
        secondary="building_heating",
        back_populates="buildings"
    )

    floor: Mapped["BuildingFloor"] = relationship(
        back_populates="building",
        uselist=False
    )

class BuildingFloor(Base):
    __tablename__ = "building_floor"
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("building.id", ondelete="CASCADE"), primary_key=True)
    floor_level: Mapped[str] = mapped_column(String)
    floor_total: Mapped[int] = mapped_column(Integer)

    building: Mapped["Building"] = relationship(
        back_populates="floor"
    )