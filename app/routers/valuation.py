import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/valuation",
    tags=["valutaion"]
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
async def check_industry(industry: str, revenue: float, cashflow: float):
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
