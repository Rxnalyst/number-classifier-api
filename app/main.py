from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

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
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        return response.json().get("text", "No fact available.")
    except:
        return "No fact available."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="The number to classify")):
    try:
        num = int(number)
    except ValueError:
        return {"number": number, "error": True}

    properties = []
    if is_armstrong(num):
        properties.append("armstrong")
    properties.append("odd" if num % 2 != 0 else "even")

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": get_digit_sum(num),
        "fun_fact": get_fun_fact(num),
    }
