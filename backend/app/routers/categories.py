# app/routers/categories.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional

from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas # Assuming you have models.py and schemas.py defined
# from app.dependencies import get_current_user # Assuming user authentication dependency

router = APIRouter()

# Pydantic models for request and response data validation
class CategoryBase(BaseModel):
    name: str = Field(..., description="Name of the transaction category (e.g., 'Groceries', 'Utilities', 'Salary')")
    type: str = Field(..., description="Type of the category (e.g., 'Expense', 'Income', 'Transfer')")
    icon: Optional[str] = Field(None, description="Optional icon or emoji for the category")
    color: Optional[str] = Field(None, description="Optional color code for the category (e.g., hexadecimal)")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: int
    user_id: int # Link to the user who owns this category
    class Config:
        orm_mode = True # For SQLAlchemy ORM compatibility

# API endpoints

# 1. Create a new category
@router.post("/", response_model=CategoryInDB, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    # db_category = models.Category(**category.dict(), user_id=current_user.id) # For authenticated users
    db_category = models.Category(**category.model_dump()) # Placeholder, replace with authenticated user's ID
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# 2. Get all categories for the current user
@router.get("/", response_model=List[CategoryInDB])
async def get_categories(
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    # categories = db.query(models.Category).filter(models.Category.user_id == current_user.id).all() # For authenticated users
    categories = db.query(models.Category).all() # Placeholder, replace with authenticated user's categories
    return categories

# 3. Get a specific category by ID
@router.get("/{category_id}", response_model=CategoryInDB)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first() # Add user_id filter for auth
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    # if category.user_id != current_user.id: # Check if category belongs to the user
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this category")
    return category

# 4. Update an existing category
@router.put("/{category_id}", response_model=CategoryInDB)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first() # Add user_id filter for auth
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    # if db_category.user_id != current_user.id: # Check if category belongs to the user
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this category")

    update_data = category_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

# 5. Delete a category
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first() # Add user_id filter for auth
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    # if db_category.user_id != current_user.id: # Check if category belongs to the user
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this category")

    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}

# 6. (Optional) Get categories by type
@router.get("/type/{category_type}", response_model=List[CategoryInDB])
async def get_categories_by_type(
    category_type: str,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    # categories = db.query(models.Category).filter(
    #     models.Category.user_id == current_user.id,
    #     models.Category.type == category_type
    # ).all()
    categories = db.query(models.Category).filter(models.Category.type == category_type).all()
    return categories
