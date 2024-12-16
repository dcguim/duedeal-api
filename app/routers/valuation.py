from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.utils.auth_flow_manager import authenticate_user
from app.utils.misc import load_json

router = APIRouter()

multiples_file_path = 'app/routers/multiples.json'
industries_file_path = 'app/routers/industries.json'

@router.get("/get-industries/")
async def get_industries(creds: dict = Depends(authenticate_user)):
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

