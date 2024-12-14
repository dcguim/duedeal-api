from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.utils.oauth_flow_manager import get_user_creds
from fastapi import HTTPException
import json

router = APIRouter()

multiples_file_path = 'app/routers/multiples.json'
industries_file_path = 'app/routers/industries.json'

def load_json(path):
    try:
        with open(path, "r") as fd:
            return json.load(fd)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="JSON file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON file")

@router.get("/get-industries/")
async def get_industries(user_info: dict = Depends(get_user_creds)):
    ind_json = load_json(industries_file_path)
    return JSONResponse(status_code=200, content=ind_json)
    
@router.get("/get-broad-valuation/")
async def generate_broad_valuation(industry: str, revenue: float, cashflow: float):
    # Load the JSON file
    mult = load_json(multiples_file_path)
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

