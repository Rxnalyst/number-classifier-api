from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NumberClassificationResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str

@app.get("/")
def root():
    return {"message": "Welcome to the Number Classification API! Use /api/classify-number?number=7"}

# Helper functions
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", timeout=5)
        response.raise_for_status()
        return response.json().get("text", "No fact available.")
    except requests.exceptions.RequestException:
        return "No fun fact available due to a network issue."

@app.get("/api/classify-number", response_model=NumberClassificationResponse)
def classify_number(number: int = Query(..., description="The number to classify")):
    logger.info(f"Received request with number: {number}")

    # Validate input: Ensure number is an integer
    if not isinstance(number, int):
        logger.error("Invalid input: Not an integer")
        raise HTTPException(status_code=400, detail="Invalid input. Must be an integer.")

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 != 0 else "even")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": get_digit_sum(number),
        "fun_fact": get_fun_fact(number),
    }

    logger.info(f"Response: {response}")
    return response
