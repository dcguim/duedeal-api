import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.users import Waitlist
from email_validator import validate_email, EmailNotValidError

router = APIRouter(
    prefix="/valuation",
    tags=["valuation"]
)

multiples_file_path = 'app/routers/multiples.json'

def load_multiples():
    try:
        with open(multiples_file_path, "r") as mult:
            return json.load(mult)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="JSON file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON file")

@router.get("/get-industries/")
async def get_industries():
    mult = load_multiples()
    industries = []
    for ind_mult in mult['multiples-bizbuysell-11-24']:
        industries.append(ind_mult['industry_sector'])
    response_mult = {'industries': industries}
    return JSONResponse(status_code=200, content=response_mult)
    
@router.get("/get-broad-valuation/")
async def generate_broad_valuation(industry: str, revenue: float, cashflow: float):
    # Load the JSON file
    mult = load_multiples()
    print(industry)
    for ind_mult in mult['multiples-bizbuysell-11-24']:
        print(ind_mult['industry_sector'])
        if industry.lower() == ind_mult['industry_sector'].lower():
             cashflow_mult = ind_mult["revenue_multiple"]*cashflow
             revenue_mult =  ind_mult["cash_flow_multiple"]*revenue
             lower_bound = min(cashflow_mult, revenue_mult)
             upper_bound = max(cashflow_mult, revenue_mult)
             response_broadval = {'broad_valuation': {'lower_bound': lower_bound,
                                                      'upper_bound': upper_bound}}
             return JSONResponse(status_code=200, content=response_broadval)

@router.post("/subscribe-waitlist/")
async def subscribe_waitlist(email: str):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

    engine = create_engine('sqlite:///duedeal.db')
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    print(inspector.get_table_names())
    
    Session = sessionmaker(bind=engine) 
    with Session() as session:
        new_user = Waitlist(email=email)
        session.add(new_user)
        # Insert the validated email into the database

        existing_user = session.query(Waitlist).filter(Waitlist.email == email).first()
        if existing_user:
            return JSONResponse(content={"error": "Email already exists."}, status_code=400)

        # Insert the new email into the database
        new_user = Waitlist(email=email)
        session.add(new_user)
        try:
            session.commit()
            return JSONResponse(content={"message": "User added successfully!"}, status_code=201)
        except Exception as e:
            session.rollback()
            return JSONResponse(content={"error": f"Unexpected error: {e}"}, status_code=500)
