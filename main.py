from fastapi import FastAPI, HTTPException
from ingredient_parser import parse_ingredient

app = FastAPI()

@app.get("/parse/")
def parse_ingredient_api(ingredient: str):
    try:
        parsed_result = parse_ingredient(ingredient)
        return {"parsed_ingredient": parsed_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
