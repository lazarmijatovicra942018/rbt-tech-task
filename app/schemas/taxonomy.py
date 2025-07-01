from pydantic import BaseModel, ConfigDict

class AmenityOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)



class HeatingOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class EstateTypeOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class OfferOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
