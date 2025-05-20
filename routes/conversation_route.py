from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from database_utility.models import Lead,timezone
from database_utility.db_connection import get_db
from database_utility.schemas import LeadCreate, LeadOut
from functionality.conversation_functionality import evaluate_lead_with_groq

router = APIRouter()

@router.post("/lead", response_model=LeadOut)
def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    relevance, message = evaluate_lead_with_groq(lead_data.conversation)

    lead = Lead(
        email=lead_data.email,
        company_name=lead_data.company_name,
        conversation=lead_data.conversation,
        lead_relevance=relevance,
        created_at=timezone
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    print(f"Returning lead relevance: {relevance}, message: {message}")

    # Always return a dictionary with the message field
    return {
        "email": lead.email,
        "company_name": lead.company_name,
        "lead_relevance": relevance,
        "conversation": lead.conversation,
        "created_at": lead.created_at,
        "message": message  # Will be "" if no meeting link needed
    }

