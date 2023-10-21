from typing import Optional
from pydantic import BaseModel

class Prediction(BaseModel):
    id : int
    animalType : str
    breed : str
    color : str
    sex : str
    status : Optional[str]
    p_animal : Optional[int]
    p_sex : Optional[int]
    p_breed : Optional[int]
    p_color : Optional[int]