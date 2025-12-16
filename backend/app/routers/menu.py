from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from app.database import SessionLocal
from app import schemas, services
from fastapi import Depends
from app.deps import admin_required
from app.models import user as user_model

router = APIRouter()

@router.post("/", response_model=schemas.DishRead)
async def create_dish(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    category: str = Form(""),
    images: Optional[List[UploadFile]] = File(None),
    current_user: user_model.User = Depends(admin_required),
):
    db = SessionLocal()
    try:
        dish_data = schemas.DishCreate(
            name=name,
            description=description,
            price=price,
            category=category
        )
        dish = services.dish_service.create_dish_with_images(db, dish_data, images,)
        return schemas.DishRead.model_validate(dish)  # ✅ сериализация
    finally:
        db.close()


@router.get("/{dish_id}", response_model=schemas.DishRead)
def read_dish(dish_id: int):
    db = SessionLocal()
    try:
        dish = services.dish_service.get_dish_by_id(db, dish_id)
        if not dish:
            raise HTTPException(status_code=404, detail="Блюдо не найдено")
        return schemas.DishRead.model_validate(dish)  # ✅ сериализация
    finally:
        db.close()


@router.get("/", response_model=List[schemas.DishRead])
def list_dishes():
    db = SessionLocal()
    try:
        dishes = services.dish_service.get_all_dishes(db)
        return [schemas.DishRead.model_validate(d) for d in dishes]  # ✅ список
    finally:
        db.close()


@router.put("/{dish_id}", response_model=schemas.DishRead)
async def update_dish(
    dish_id: int,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    category: str = Form(""),
    images: Optional[List[UploadFile]] = File(None),
    current_user: user_model.User = Depends(admin_required),
):
    db = SessionLocal()
    try:
        dish_data: schemas.DishCreate = schemas.DishCreate(
            name=name,
            description=description,
            price=price,
            category=category
        )

        updated_dish = services.dish_service.update_dish(db, dish_id, dish_data, images)
        if not updated_dish:
            raise HTTPException(status_code=404, detail="Блюдо не найдено")
        return schemas.DishRead.model_validate(updated_dish)  # ✅ сериализация
    finally:
        db.close()


@router.delete("/{dish_id}", response_model=schemas.DishRead)
async def delete_dish(
    dish_id: int,
    current_user: user_model.User = Depends(admin_required),
):
    db = SessionLocal()
    try:
        dish = services.dish_service.delete_dish(db, dish_id)
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        return dish
    finally:
        db.close()

@router.get("/category/{category_name}", response_model=List[schemas.DishRead])
def get_dishes_by_category_name(category_name: str):
    db = SessionLocal()
    return services.dish_service.get_dishes_by_category_name(db, category_name)