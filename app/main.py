from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import math

app = FastAPI()

class NumberResponse(BaseModel):
    number: float
    is_even: bool
    is_prime: bool | None = None  # Prime numbers must be integers
    is_armstrong: bool | None = None  # Armstrong check is integer-only

def is_prime(n):
    if n < 2 or not n.is_integer():
        return None  # Floats aren't prime
    n = int(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    if not n.is_integer():
        return None  # Armstrong only valid for integers
    digits = [int(d) for d in str(abs(int(n)))]
    return sum(d ** len(digits) for d in digits) == abs(int(n))

@app.get("/api/classify-number", response_model=NumberResponse)
async def classify_number(number: str):
    try:
        num = float(number)
    except ValueError:
        raise HTTPException(status_code=400, detail=json.dumps({"error": "Invalid input", "number": number}))

    return {
        "number": num,
        "is_even": num % 2 == 0,
        "is_prime": is_prime(num),
        "is_armstrong": is_armstrong(num),
    }
