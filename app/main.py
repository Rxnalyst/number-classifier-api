from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import math

app = FastAPI()

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
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(abs(n))]
    length = len(digits)
    return sum(d ** length for d in digits) == abs(n)

def digit_sum(n: int) -> int:
    """Calculate the sum of digits of a number."""
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n: int) -> str:
    """Generate a fun fact about a number."""
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join([f'{d}^{len(str(abs(n)))}' for d in str(abs(n))])} = {n}"
    return f"{n} is a fascinating number with unique properties."

def classify_properties(n: int) -> list:
    """Classify number properties (Armstrong, Odd, Even)."""
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties

@app.get("/api/classify-number")
async def classify_number(number: str = Query(...)):
    try:
        number_int = int(number)  # Convert to integer
    except ValueError:
        return JSONResponse(status_code=400, content={"number": number, "error": True})  # Return correct 400 error format

    response = {
        "number": number_int,
        "is_prime": is_prime(number_int),
        "is_perfect": is_perfect(number_int),
        "properties": classify_properties(number_int),
        "digit_sum": digit_sum(number_int),
        "fun_fact": get_fun_fact(number_int),
    }
    return response
