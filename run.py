#!/usr/bin/env python3
"""
Air Quality Prediction Website - Startup Script
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'matplotlib', 'seaborn', 'joblib'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print("   pip install -r requirements.txt")
            return False
    
    return True

def check_dataset():
    """Check if air_quality.csv exists, create sample if not"""
    if not os.path.exists('air_quality.csv'):
        print("📊 Dataset not found. Creating sample dataset...")
        try:
            from create_sample_data import create_sample_dataset
            sample_df = create_sample_dataset()
            sample_df.to_csv('air_quality.csv', index=False)
            print("✅ Sample dataset created successfully!")
            print(f"   Dataset shape: {sample_df.shape}")
            print(f"   Records: {len(sample_df)}")
        except Exception as e:
            print(f"❌ Failed to create sample dataset: {e}")
            return False
    else:
        print("✅ Dataset found: air_quality.csv")
    
    return True

def main():
    """Main startup function"""
    print("🌿 Air Quality Prediction Website")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check dataset
    if not check_dataset():
        return
    
    print("\n🚀 Starting the application...")
    print("   The website will be available at: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the Flask application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main() 