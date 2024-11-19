from pydantic import BaseModel, EmailStr, constr

class UserCreateSchema(BaseModel):
    username: constr(min_length=3, max_length=150)  # Ensuring username length
    email: EmailStr  # Automatically validates email format
    password: constr(min_length=6)  # Ensure password is at least 6 characters

    class Config:
        # Enforce extra fields validation (reject unknown fields in incoming requests)
        extra = "forbid"

# Pydantic schema for updating a user
class UserUpdateSchema(BaseModel):
    username: constr(min_length=3, max_length=150) = None
    email: EmailStr = None
    password: constr(min_length=6) = None

    class Config:
        extra = "forbid"