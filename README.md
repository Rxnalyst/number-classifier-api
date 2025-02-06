# Number Classification API

## Overview
A simple API that classifies numbers based on mathematical properties.

## Features
- Checks if a number is prime, perfect, or Armstrong
- Determines if the number is odd or even
- Computes the sum of its digits
- Fetches a fun mathematical fact

## API Endpoint
### `GET /api/classify-number?number=<integer>`
#### Example Response:
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
