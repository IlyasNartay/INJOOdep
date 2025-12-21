from sqlalchemy.orm import Session, joinedload
from typing import List
import shutil
import uuid
import os

from app import models, schemas

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_files(files: List, dish_id: int) -> List[models.DishImage]:
    image_models = []
    for file in files:
        ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_url = os.path.join(UPLOAD_DIR, filename)

        with open(file_url, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_models.append(models.DishImage(image_url=file_url.replace("\\", "/"), dish_id=dish_id))
    return image_models


def create_dish_with_images(db: Session, dish_data: schemas.DishCreate, images) -> schemas.DishRead:
    dish = models.Dish(**dish_data.dict())
    db.add(dish)
    db.commit()
    db.refresh(dish)

    if images:
        image_models = save_uploaded_files(images, dish.id)
        db.add_all(image_models)
        db.commit()

    db.refresh(dish)
    return schemas.DishRead.model_validate(dish)


def get_dish_by_id(db: Session, dish_id: int) -> schemas.DishRead | None:
    dish = db.query(models.Dish) \
        .options(joinedload(models.Dish.images)) \
        .filter(models.Dish.id == dish_id) \
        .first()

    if dish:
        return schemas.DishRead.model_validate(dish)
    return None


def get_all_dishes(db: Session) -> List[schemas.DishRead]:
    dishes = db.query(models.Dish).options(joinedload(models.Dish.images)).all()
    return [schemas.DishRead.model_validate(dish) for dish in dishes]

def update_dish_availability(db, dish_id: int, available: bool):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        return None

    dish.available = available
    db.commit()
    db.refresh(dish)
    return dish

def update_dish(db: Session, dish_id: int, dish_data: schemas.DishCreate, images=None) -> schemas.DishRead | None:
    dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if not dish:
        return None

    # Обновление только изменённых полей
    for key, value in dish_data.dict(exclude_unset=True).items():
        current_value = getattr(dish, key)
        if value != current_value:
            setattr(dish, key, value)

    # Обновляем изображения только если они переданы
    if images:
        old_images = db.query(models.DishImage).filter(models.DishImage.dish_id == dish_id).all()
        for img in old_images:
            if os.path.exists(img.image_url):
                os.remove(img.image_url)
        db.query(models.DishImage).filter(models.DishImage.dish_id == dish_id).delete()

        image_models = save_uploaded_files(images, dish_id)
        db.add_all(image_models)

    db.commit()
    db.refresh(dish)

    return schemas.DishRead.model_validate(dish)



def delete_dish(db: Session, dish_id: int) -> schemas.DishRead:
    dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if not dish:
        return None

    # Удалить изображения и файлы
    images = db.query(models.DishImage).filter(models.DishImage.dish_id == dish_id).all()
    for img in images:
        if os.path.exists(img.image_url):
            os.remove(img.image_url)

    db.query(models.DishImage).filter(models.DishImage.dish_id == dish_id).delete()
    db.delete(dish)
    db.commit()
    return dish

def get_dishes_by_category_name(db: Session, category_name: str) -> List[schemas.DishRead]:
    dishes = (
        db.query(models.Dish)
        .options(joinedload(models.Dish.images))
        .filter(models.Dish.category == category_name)
        .all()
    )
    return [schemas.DishRead.model_validate(dish) for dish in dishes]


