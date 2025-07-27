import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os
from flask import Flask, render_template, request, jsonify
import json
import base64
from io import BytesIO

app = Flask(__name__)

# Global variables to store model and metrics
model = None
model_metrics = {}
feature_importances = {}

def train_model():
    """Train the Random Forest model and save it"""
    global model, model_metrics, feature_importances
    
    # Load dataset
    df = pd.read_csv('aqi.csv', na_values=['NA'])
    
    # Drop rows where target (pm2.5) is missing
    df = df.dropna(subset=['pm2.5'])
    
    # Create datetime feature
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce')
    df = df.dropna(subset=['datetime'])
    df.set_index('datetime', inplace=True)
    
    # Add lag feature: previous hour's pm2.5
    df['pm2.5_lag1'] = df['pm2.5'].shift(1)
    df.dropna(inplace=True)
    
    # Prepare features
    features = ['DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'cbwd', 'hour', 'month', 'pm2.5_lag1']
    target = 'pm2.5'
    
    X = df[features]
    y = df[target]
    
    # Define categorical and numerical features
    categorical = ['cbwd']
    numerical = [col for col in features if col not in categorical]
    
    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), numerical),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical)
        ])
    
    # Define the model
    rf = RandomForestRegressor(random_state=42)
    
    # Full pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', rf)
    ])
    
    # Train/test split
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Hyperparameter tuning
    param_grid = {
        'regressor__n_estimators': [100, 150],
        'regressor__max_depth': [10, 20, None],
        'regressor__min_samples_split': [2, 5]
    }
    
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train_raw, y_train)
    
    # Best model and predictions
    model = grid_search.best_estimator_
    y_pred = model.predict(X_test_raw)
    
    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = np.mean(np.abs(y_test - y_pred))
    
    model_metrics = {
        'r2_score': round(r2, 4),
        'rmse': round(rmse, 4),
        'mae': round(mae, 4),
        'best_params': grid_search.best_params_
    }
    
    # Feature importance
    final_model = model.named_steps['regressor']
    feature_names = numerical + list(model.named_steps['preprocessor'].transformers_[1][1].get_feature_names_out(['cbwd']))
    importances = final_model.feature_importances_
    
    feature_importances = dict(zip(feature_names, importances))
    
    # Save model
    joblib.dump(model, 'air_quality_model.pkl')
    # Save metrics and feature importances
    with open('model_metrics.json', 'w') as f:
        json.dump(model_metrics, f)
    with open('feature_importances.json', 'w') as f:
        json.dump(feature_importances, f)
    # Create and save visualizations
    create_visualizations(X_test_raw, y_test, y_pred, feature_importances)
    
    return model_metrics

def create_visualizations(X_test, y_test, y_pred, feature_importances):
    """Create and save visualizations"""
    # Set style
    plt.style.use('default')
    
    # 1. Feature Importance Plot
    plt.figure(figsize=(12, 8))
    features = list(feature_importances.keys())
    importances = list(feature_importances.values())
    
    # Sort by importance
    sorted_idx = np.argsort(importances)
    features_sorted = [features[i] for i in sorted_idx]
    importances_sorted = [importances[i] for i in sorted_idx]
    
    plt.barh(range(len(features_sorted)), importances_sorted)
    plt.yticks(range(len(features_sorted)), features_sorted)
    plt.xlabel('Feature Importance')
    plt.title('Random Forest Feature Importance')
    plt.tight_layout()
    plt.savefig('static/images/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Actual vs Predicted Plot
    plt.figure(figsize=(10, 8))
    plt.scatter(y_test, y_pred, alpha=0.6, color='blue')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual PM2.5')
    plt.ylabel('Predicted PM2.5')
    plt.title('Actual vs Predicted PM2.5 Values')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/images/actual_vs_predicted.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Residuals Plot
    residuals = y_test - y_pred
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(y_pred, residuals, alpha=0.6, color='green')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted PM2.5')
    plt.ylabel('Residuals')
    plt.title('Residuals vs Predicted Values')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.hist(residuals, bins=30, alpha=0.7, color='orange', edgecolor='black')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Residuals')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('static/images/residuals_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def predict_air_quality(input_data):
    """Make prediction using the trained model"""
    try:
        # Create a DataFrame with the input data
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return round(prediction, 2)
    except Exception as e:
        print(f"Prediction error: {e}")  # Log error
        return None

@app.route('/')
def home():
    return render_template('index.html', metrics=model_metrics, feature_importances=feature_importances)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract input values
        input_data = {
            'DEWP': float(data['DEWP']),
            'TEMP': float(data['TEMP']),
            'PRES': float(data['PRES']),
            'Iws': float(data['Iws']),
            'Is': float(data['Is']),
            'Ir': float(data['Ir']),
            'cbwd': data['cbwd'],
            'hour': int(data['hour']),
            'month': int(data['month']),
            'pm2.5_lag1': float(data['pm2_5_lag1'])
        }
        
        # Make prediction
        prediction = predict_air_quality(input_data)
        
        if prediction is not None:
            return jsonify({
                'success': True,
                'prediction': prediction,
                'message': f'Predicted PM2.5: {prediction} μg/m³'
            })
        else:
            print('Prediction returned None')  # Log error
            return jsonify({
                'success': False,
                'message': 'Error making prediction'
            })
            
    except Exception as e:
        print(f"/predict endpoint error: {e}")  # Log error
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # Create static/images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    # Train model if it doesn't exist
    if not os.path.exists('air_quality_model.pkl'):
        print("Training model...")
        model_metrics = train_model()
        print("Model trained and saved!")
        # feature_importances is set in train_model
    else:
        # Load existing model
        model = joblib.load('air_quality_model.pkl')
        # Load metrics and feature importances if available
        if os.path.exists('model_metrics.json'):
            with open('model_metrics.json', 'r') as f:
                model_metrics = json.load(f)
        if os.path.exists('feature_importances.json'):
            with open('feature_importances.json', 'r') as f:
                feature_importances = json.load(f)
    app.run(debug=True, host='0.0.0.0', port=5000) 