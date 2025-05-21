# MTCars Flask API

A Flask API that predicts car MPG (Miles Per Gallon) using the MTCars dataset. The API uses Linear Regression for predictions and K-means clustering for grouping similar cars.

## Quick Start

### Using Docker
```bash
docker pull yzong17/mtcars_flask_api:latest
# For local testing (port 8001)
docker run -d -p 8001:8001 yzong17/mtcars_flask_api:latest
# For cloud platforms (using PORT environment variable)
docker run -d -p 8080:8080 -e PORT=8080 yzong17/mtcars_flask_api:latest
```

### Local Setup
```bash
pip install -r requirements.txt
python model.py  # Defaults to port 8001
# Or specify a custom port:
PORT=8080 python model.py
```

### Cloud Run Deployment
```bash
# Deploy to Cloud Run
gcloud run deploy mtcars-flask-api \
  --image yzong17/mtcars_flask_api:latest \
  --platform managed \
  --allow-unauthenticated
```

## API Endpoints

- GET `/features`: List available car features
- POST `/predict`: Predict MPG for a car

### Example Usage
```bash
# For local testing
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cyl": 6,
    "disp": 160,
    "hp": 110,
    "drat": 3.9,
    "wt": 2.62,
    "qsec": 16.46,
    "vs": 0,
    "am": 1,
    "gear": 4,
    "carb": 4
  }'

# For Cloud Run (replace URL with your service URL)
curl -X POST https://your-service-url/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cyl": 6,
    "disp": 160,
    "hp": 110,
    "drat": 3.9,
    "wt": 2.62,
    "qsec": 16.46,
    "vs": 0,
    "am": 1,
    "gear": 4,
    "carb": 4
  }'
```

The API will return the predicted MPG and a cluster assignment (0-2) for the car. 