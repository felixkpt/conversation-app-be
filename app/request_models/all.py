from pydantic import BaseModel, Field, validator

# Define request models

class CategoryRequest(BaseModel):
    name: str = Field(..., description="Category name is required")
    description: str = Field(...,
                             description="Category description is required")

    @validator("name")
    def name_must_have_at_least_one_character(cls, v):
        if not v.strip():
            raise ValueError("Name must have at least one character")
        return v

    @validator("description")
    def description_must_have_at_least_one_character(cls, v):
        if not v.strip():
            raise ValueError("Description must have at least one character")
        return v


class SubCategoryRequest(BaseModel):
    name: str
    slug: str | None
    learn_instructions: str
