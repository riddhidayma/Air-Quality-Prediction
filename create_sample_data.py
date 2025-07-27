import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_dataset():
    """Create a sample air quality dataset for testing"""
    
    # Generate date range
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Create base DataFrame
    df = pd.DataFrame({
        'datetime': date_range,
        'year': date_range.year,
        'month': date_range.month,
        'day': date_range.day,
        'hour': date_range.hour
    })
    
    # Generate realistic environmental data
    np.random.seed(42)  # For reproducible results
    
    # Temperature (seasonal pattern with daily variation)
    base_temp = 15 + 10 * np.sin(2 * np.pi * (df['month'] - 1) / 12)  # Seasonal
    daily_temp = 5 * np.sin(2 * np.pi * df['hour'] / 24)  # Daily
    temp_noise = np.random.normal(0, 3, len(df))
    df['TEMP'] = base_temp + daily_temp + temp_noise
    
    # Dew point (related to temperature)
    df['DEWP'] = df['TEMP'] - np.random.uniform(5, 15, len(df))
    
    # Pressure (slight seasonal variation)
    base_pressure = 1013 + 10 * np.sin(2 * np.pi * (df['month'] - 1) / 12)
    pressure_noise = np.random.normal(0, 5, len(df))
    df['PRES'] = base_pressure + pressure_noise
    
    # Wind speed (higher in winter)
    base_wind = 8 + 4 * np.sin(2 * np.pi * (df['month'] - 1) / 12)
    wind_noise = np.random.exponential(2, len(df))
    df['Iws'] = np.maximum(0, base_wind + wind_noise)
    
    # Wind direction (categorical)
    wind_directions = ['NW', 'NE', 'SW', 'SE', 'cv']
    df['cbwd'] = np.random.choice(wind_directions, len(df), p=[0.3, 0.2, 0.2, 0.2, 0.1])
    
    # Precipitation (more in summer)
    rain_prob = 0.1 + 0.2 * np.sin(2 * np.pi * (df['month'] - 6) / 12)
    df['Ir'] = np.where(np.random.random(len(df)) < rain_prob, 
                       np.random.exponential(2, len(df)), 0)
    
    # Snow (winter months only)
    snow_prob = np.where(df['month'].isin([12, 1, 2]), 0.05, 0)
    df['Is'] = np.where(np.random.random(len(df)) < snow_prob,
                       np.random.exponential(1, len(df)), 0)
    
    # Generate PM2.5 with realistic patterns
    # Base PM2.5 with seasonal and daily patterns
    base_pm25 = 30 + 20 * np.sin(2 * np.pi * (df['month'] - 1) / 12)  # Higher in winter
    daily_pm25 = 10 * np.sin(2 * np.pi * df['hour'] / 24)  # Daily variation
    
    # Add correlation with other features
    temp_effect = -0.5 * df['TEMP']  # Higher temp = lower PM2.5
    wind_effect = -2 * df['Iws']  # Higher wind = lower PM2.5
    pressure_effect = 0.02 * (df['PRES'] - 1013)  # Pressure effect
    
    # Combine all effects
    pm25_base = base_pm25 + daily_pm25 + temp_effect + wind_effect + pressure_effect
    
    # Add some extreme events (occasional high pollution)
    extreme_events = np.random.random(len(df)) < 0.02  # 2% chance
    pm25_extreme = np.where(extreme_events, np.random.uniform(100, 200, len(df)), 0)
    
    # Add noise
    pm25_noise = np.random.normal(0, 8, len(df))
    
    # Final PM2.5 values
    df['pm2.5'] = np.maximum(0, pm25_base + pm25_extreme + pm25_noise)
    
    # Add some missing values (NA) to simulate real data
    missing_mask = np.random.random(len(df)) < 0.05  # 5% missing values
    df.loc[missing_mask, 'pm2.5'] = np.nan
    
    # Reorder columns to match expected format
    column_order = ['year', 'month', 'day', 'hour', 'pm2.5', 'DEWP', 'TEMP', 'PRES', 'cbwd', 'Iws', 'Is', 'Ir']
    df = df[column_order]
    
    return df

if __name__ == "__main__":
    # Create sample dataset
    sample_df = create_sample_dataset()
    
    # Save to CSV
    sample_df.to_csv('air_quality.csv', index=False)
    
    print("Sample dataset created successfully!")
    print(f"Dataset shape: {sample_df.shape}")
    print(f"Date range: {sample_df['year'].min()}-{sample_df['month'].min()}-{sample_df['day'].min()} to {sample_df['year'].max()}-{sample_df['month'].max()}-{sample_df['day'].max()}")
    print(f"Missing PM2.5 values: {sample_df['pm2.5'].isna().sum()}")
    print("\nFirst few rows:")
    print(sample_df.head())
    print("\nDataset statistics:")
    print(sample_df.describe()) 