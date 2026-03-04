from pydantic import BaseModel,Field

class KeepNote(BaseModel):
    Title:str
    Progress:str=Field(...,description='TO Do,In Progress,Done')
    Description:str




