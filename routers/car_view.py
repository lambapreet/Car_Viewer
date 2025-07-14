from fastapi import APIRouter, Query, Path, HTTPException, status, Body
from typing import List, Dict, Optional
from ..models import CarModel
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix='/cars',
    tags=['Car View']
)

# Example in-memory DB
get_db: Dict[int, CarModel] = {
    1: CarModel(id=1, brand="Toyota", model="Camry", year=2020),
    2: CarModel(id=2, brand="Honda", model="Civic", year=2021),
    3: CarModel(id=3, brand="Ford", model="Mustang", year=2019),
}

@router.get('/')
def root():
    return {"Message": "Cars"}

@router.get('/all', response_model=List[Dict[str, CarModel]])
def get_cars(number: Optional[str] = Query("10", max_length=3)):
    response = []
    for id, car in list(get_db.items())[:int(number)]:
        response.append({str(id): car})
    return response

@router.get("/{id}", response_model=CarModel)
def get_car(id: int = Path(..., ge=0, lt=1000)):
    car = get_db.get(id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    return car

@router.post('/', status_code=status.HTTP_201_CREATED)
def add_car(body_cars: List[CarModel], mind_id: Optional[int] = Body(0)):
    if len(body_cars) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No cars added")
    mind_id = len(get_db) + mind_id
    for car in body_cars:
        while get_db.get(mind_id):
            mind_id += 1
        get_db[mind_id] = car
        mind_id += 1
    return {"message": "Cars added successfully"}

@router.put('/{id}', response_model=Dict[str, CarModel])
def update_car(id: int, car: CarModel = Body(...)):
    stored = get_db.get(id)
    if not stored:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    
    updated_car = car.copy(update=car.dict(exclude_unset=True))
    get_db[id] = updated_car
    return {str(id): updated_car}

@router.delete('/{id}')
def delete_car(id: int):
    if not get_db.get(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    del get_db[id]
    return {"message": "Car deleted successfully"}
