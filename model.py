import os
os.environ['MPLBACKEND'] = 'Agg'

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class MPGPredictor:
    def __init__(self):
        self.model = None
        self.kmeans = None
        self.scaler = None
        self.feature_names = None
        self.train_model()
    
    def train_model(self):
        # Read the dataset
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data = pd.read_csv(os.path.join(current_dir, 'mtcars.csv'))
        
        # Prepare features (X) and target (y)
        X = self.data.drop(['mpg', 'model'], axis=1)
        y = self.data['mpg']
        
        # Save feature names for validation
        self.feature_names = X.columns.tolist()
        
        # Scale the features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the linear regression model
        self.model = LinearRegression()
        self.model.fit(X, y)
        
        # Train k-means model (using 3 clusters)
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        self.kmeans.fit(X_scaled)
        
        # Calculate and print model performance
        y_pred = self.model.predict(X)
        mse = np.mean((y - y_pred) ** 2)
        r2 = self.model.score(X, y)
        print(f"Model trained with MSE: {mse:.2f}, R2: {r2:.2f}")
    
    def predict(self, features):
        """
        Make MPG prediction
        
        Args:
            features (dict): Dictionary containing car features
            
        Returns:
            tuple: (predicted_mpg, cluster)
        """
        # Remove empty inputs
        features = {k: v for k, v in features.items() if v is not None and v != ""}
        
        # Check if we have enough features
        if len(features) < 2:
            raise ValueError("Please provide at least 2 features for prediction")
        
        # Create input data with available features
        input_data = pd.DataFrame([features])
        
        # Fill missing features with median values from training data
        for feat in self.feature_names:
            if feat not in features:
                input_data[feat] = self.data[feat].median()
        
        # Reorder columns to match training data
        input_data = input_data[self.feature_names]
        
        # Make prediction
        prediction = self.model.predict(input_data)[0]
        
        # Get cluster for new data point
        input_scaled = self.scaler.transform(input_data)
        cluster = self.kmeans.predict(input_scaled)[0]
        
        return round(float(prediction), 2), int(cluster)
    
    def get_feature_names(self):
        """Return list of required feature names"""
        return self.feature_names

# Initialize the model
predictor = MPGPredictor()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = request.json
        prediction, cluster = predictor.predict(features)
        return jsonify({
            'prediction': prediction,
            'cluster': cluster,
            'status': 'success'
        })
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred',
            'status': 'error'
        }), 500

@app.route('/features', methods=['GET'])
def get_features():
    try:
        features = predictor.get_feature_names()
        return jsonify({
            'features': features,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port) 