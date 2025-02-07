from fastapi import FastAPI, Query
import requests

app = FastAPI()

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def sum_of_digits(n):
    return sum(int(digit) for digit in str(n))

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    if not number.isdigit():
        return {"number": number, "error": True}

    num = int(number)
    properties = []
    
    if num % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    if is_prime(num):
        properties.append("prime")

    if is_perfect(num):
        properties.append("perfect")

    if is_armstrong(num):
        properties.append("armstrong")

    fun_fact = requests.get(f"http://numbersapi.com/{num}").text

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "class_sum": sum_of_digits(num),
        "fun_fact": fun_fact
    }
