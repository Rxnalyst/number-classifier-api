Number Classification API

Overview

This API classifies numbers based on different mathematical properties such as prime, perfect, Armstrong, and odd/even. It also provides a fun fact about the number.

Base URL

<your-deployment-url>

Endpoint

GET /api/classify-number?number={integer}

Request Parameters

Parameter

Type

Description

number

int

The integer to classify.

Success Response (200 OK)

{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

Error Response (400 Bad Request)

{
    "number": "alphabet",
    "error": true
}

Features

Checks if a number is prime

Checks if a number is perfect

Checks if a number is Armstrong

Determines if a number is odd/even

Computes the sum of its digits

Provides a fun fact about the number

Installation

Clone this repository:

git clone <repo-url>
cd <repo-folder>

Install dependencies:

pip install -r requirements.txt

Run the API:

uvicorn app.main:app --host 0.0.0.0 --port 8000

Deployment

To deploy the API publicly:

Use Render, Vercel, AWS Lambda, or any cloud provider.

Ensure the API is accessible via a public URL.

Response time should be < 500ms for optimal performance.
