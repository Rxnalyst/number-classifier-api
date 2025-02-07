from fastapi import FastAPI, Query
from typing import Dict, Any
import math

app = FastAPI()

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n < 2:
        return False
    sum_divisors = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    length = len(digits)
    return sum(d ** length for d in digits) == abs(n)

def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n: int) -> str:
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join([f'{d}^{len(str(abs(n)))}' for d in str(abs(n))])} = {n}"
    return f"{n} is a fascinating number with unique properties."

def classify_properties(n: int) -> list:
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties

@app.get("/api/classify-number", response_model=Dict[str, Any])
def classify_number(number: int = Query(..., description="The number to classify")):
    try:
        response = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": classify_properties(number),
            "digit_sum": digit_sum(number),
            "fun_fact": get_fun_fact(number)
        }
        return response
    except Exception as e:
        return {"error": True, "message": str(e)}

@app.get("/api/classify-number", response_model=Dict[str, Any])
def handle_invalid_input(number: str):
    return {"number": number, "error": True}
