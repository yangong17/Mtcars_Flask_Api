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

### Building for Cloud Platforms
```bash
# Build for AMD64 (required for Google Cloud Run)
docker buildx build --platform linux/amd64 \
  -t yzong17/mtcars_flask_api \
  --push .
```

### Local Setup
```bash
pip install -r requirements.txt
python model.py  # Defaults to port 8001
# Or specify a custom port:
PORT=8080 python model.py
```

### Cloud Run Deployment
The API is deployed at: https://mtcars-flask-api-228019890474.us-central1.run.app

## API Endpoints

- GET `/`: Health check endpoint
- GET `/features`: List available car features
- POST `/predict`: Predict MPG for a car

### Example Usage

#### Local Testing
```bash
# Health check
curl http://localhost:8001/

# Get features
curl http://localhost:8001/features

# Make prediction
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
```

#### Cloud Run
```bash
# Health check
curl https://mtcars-flask-api-228019890474.us-central1.run.app/

# Get features
curl https://mtcars-flask-api-228019890474.us-central1.run.app/features

# Make prediction
curl -X POST https://mtcars-flask-api-228019890474.us-central1.run.app/predict \
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