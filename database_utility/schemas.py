from typing import Optional
from pydantic import BaseModel, EmailStr

class LeadCreate(BaseModel):
    email: EmailStr
    company_name: str
    conversation: str

class LeadOut(BaseModel):
    email: str
    company_name: str
    lead_relevance: str
    message: Optional[str] = ""