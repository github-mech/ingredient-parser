import os
import subprocess
from fastapi import FastAPI, HTTPException

# Install ingredient-parser manually
if not os.path.exists("ingredient-parser"):
    subprocess.run(["git", "clone", "https://github.com/strangetom/ingredient-parser.git"], check=True)

# Import from the cloned repository
import sys
sys.path.insert(0, "ingredient-parser")

from ingredient_parser import parse_ingredient

app = FastAPI()

@app.get("/parse/")
def parse_ingredient_api(ingredient: str):
    try:
        parsed_result = parse_ingredient(ingredient)
        return {"parsed_ingredient": parsed_result}
    except ImportError:
        raise HTTPException(status_code=500, detail="Ingredient Parser is not installed correctly.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
