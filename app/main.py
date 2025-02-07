from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

class NumberResponse(BaseModel):
    number: Union[int, float, str]
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n <= 0:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_number_properties(n: int) -> List[str]:
    properties = ["even" if n % 2 == 0 else "odd"]
    if is_prime(n):
        properties.append("prime")
    return properties

def get_fun_fact(n: int) -> str:
    return f"{n} is a special number."

@app.get("/api/classify-number", response_model=NumberResponse)
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        number = float(number)  # Convert input to float
        number_int = int(number) if number.is_integer() else number  # Convert to int if whole number
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "number": number,  # Show the invalid input
                "error": "Invalid number input",
                "message": "Please provide a valid integer or floating-point number."
            }
        )

    response_data = {
        "number": number,
        "is_prime": is_prime(number_int),
        "is_perfect": is_perfect(number_int),
        "properties": get_number_properties(number_int),
        "digit_sum": sum(map(int, str(abs(number_int)))),
        "fun_fact": get_fun_fact(number_int),
    }

    return response_data  # FastAPI will handle JSON conversion
