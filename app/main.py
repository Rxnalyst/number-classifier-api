import json
import math

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
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

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(abs(n))]
    length = len(digits)
    return sum(d ** length for d in digits) == abs(n)

def digit_sum(n):
    """Calculate the sum of digits of a number."""
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n):
    """Generate a fun fact about a number."""
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join([f'{d}^{len(str(abs(n)))}' for d in str(abs(n))])} = {n}"
    return f"{n} is a fascinating number with unique properties."

def classify_properties(n):
    """Classify number properties (armstrong, odd, even)."""
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties


def lambda_handler(event, context):
    try:
        print("🔍 Received event:", json.dumps(event))  # Log incoming request

        query_params = event.get("queryStringParameters", {})

        if not query_params or "number" not in query_params:
            print("❌ ERROR: Missing number parameter")
            return create_response(400, {"number": None, "error": "Missing number parameter"})

        number_str = query_params.get("number")
        print("📌 Extracted number:", number_str)  # Log extracted number

        try:
            number = float(number_str)  # Convert input to float
        except ValueError:
            print("❌ ERROR: Invalid number format:", number_str)
            return create_response(400, {"number": number_str, "error": "Invalid number format"})

        is_whole = number.is_integer()
        int_number = int(number) if is_whole else None

        if is_whole:  # ✅ Whole numbers (including negative)
            response = {
                "number": number,
                "is_prime": is_prime(int_number) if int_number > 0 else False,
                "is_perfect": is_perfect(int_number) if int_number > 0 else False,
                "properties": classify_properties(int_number),
                "digit_sum": digit_sum(abs(int_number)),  # ✅ Ensure digit sum is always a number
                "fun_fact": get_fun_fact(int_number) if int_number > 0 else f"{number} is a negative number with unique properties."
            }
        else:  # ✅ Floating-Point Numbers
            response = {
                "number": number,
                "is_prime": False,
                "is_perfect": False,
                "properties": [],
                "digit_sum": digit_sum(int(number)),  # ✅ Convert float to integer for digit sum
                "fun_fact": f"{number} is a real number with unique properties."
            }

        print("✅ SUCCESS: Returning response:", response)  # Log final response
        return create_response(200, response)

    except Exception as e:
        print("❌ ERROR: Internal server error:", str(e))
        return create_response(500, {"number": None, "error": "Internal server error", "message": str(e)})


def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps(body)
    }