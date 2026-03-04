from pydantic import BaseModel,field_validator,model_validator

class Userdetails(BaseModel):
    name:str
    email:str
    password:str

    @field_validator('password')
    def valid_length(cls,v):
        if len(v)<8:
            raise ValueError("Password must be at least 8 characters")
        
        return v
class Userinfo(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordUpdate(BaseModel):
    current_password:str
    new_password:str
    confirm_password:str

    @field_validator('new_password')
    def valid_password(cls,v):
        if len(v)<8:
            raise ValueError("Password must be at least 8 characters")
        
        return v
        
        return v
    @model_validator(mode='after')
    def check_password(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Password didn't match confirm password")
        return self
    
    