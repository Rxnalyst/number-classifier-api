from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union
import math

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NumberResponse(BaseModel):
    number: Union[int, float]
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n <= 0:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_number_properties(n: int) -> List[str]:
    """Get properties of the number."""
    properties = ["even" if n % 2 == 0 else "odd"]
    if is_prime(n):
        properties.append("prime")
    return properties

def get_fun_fact(n: int) -> str:
    """Generate a fun fact about the number."""
    return f"{n} is a unique number with special properties."

@app.get("/")
async def root():
    return {"message": "Welcome to the Number Classification API!"}

@app.get("/api/classify-number", response_model=NumberResponse)
async def classify_number(number: Union[int, float] = Query(..., description="The number to classify")):
    try:
        response_data = {
            "number": number,
            "is_prime": is_prime(int(number)),
            "is_perfect": is_perfect(int(number)),
            "properties": get_number_properties(int(number)),
            "digit_sum": sum(map(int, str(abs(int(number))))),
            "fun_fact": get_fun_fact(int(number)),
        }
        return response_data
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid number format")

@app.get("/health")
async def health_check():
    """Health check endpoint for Render deployment."""
    return {"status": "ok"}
