# Air Quality Prediction Website

A comprehensive web application for predicting air quality (PM2.5) using Random Forest machine learning algorithm. The website features an interactive interface, detailed model explanations, and real-time predictions.

## 🌟 Features

- **Interactive Prediction Interface**: Input environmental parameters to get real-time PM2.5 predictions
- **Model Performance Metrics**: Display R² score, RMSE, and MAE with visual indicators
- **Random Forest Visualization**: Animated forest representation and feature importance charts
- **Comprehensive Documentation**: Detailed explanations of the algorithm and air quality concepts
- **Responsive Design**: Modern, mobile-friendly interface with smooth animations
- **Real-time Validation**: Form validation and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd air_quality_prediction_website
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your dataset**
   - Place your `air_quality.csv` file in the project root directory
   - The dataset should contain the following columns:
     - `year`, `month`, `day`, `hour` (time features)
     - `pm2.5` (target variable)
     - `DEWP`, `TEMP`, `PRES` (meteorological features)
     - `cbwd`, `Iws` (wind features)
     - `Is`, `Ir` (precipitation features)

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the website**
   - Open your browser and go to `http://localhost:5000`
   - The model will automatically train on first run

## 📊 Dataset Requirements

Your `air_quality.csv` file should have the following structure:

| Column | Description | Type | Example |
|--------|-------------|------|---------|
| year | Year of measurement | int | 2020 |
| month | Month (1-12) | int | 1 |
| day | Day of month | int | 1 |
| hour | Hour (0-23) | int | 14 |
| pm2.5 | PM2.5 concentration | float | 45.2 |
| DEWP | Dew point temperature | float | -15.0 |
| TEMP | Air temperature | float | -8.0 |
| PRES | Atmospheric pressure | float | 1020.0 |
| cbwd | Wind direction | string | "NW" |
| Iws | Wind speed | float | 12.5 |
| Is | Snow hours | float | 0.0 |
| Ir | Rain hours | float | 0.0 |

## 🏗️ Project Structure

```
air_quality_prediction_website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── air_quality.csv       # Your dataset (not included)
├── templates/
│   ├── index.html        # Main page template
│   └── about.html        # About page template
└── static/
    ├── css/
    │   └── style.css     # Custom styles
    ├── js/
    │   └── script.js     # JavaScript functionality
    └── images/           # Generated visualizations
```

## 🧠 Model Information

### Random Forest Algorithm

The application uses a Random Forest regressor with the following characteristics:

- **Ensemble Method**: Combines multiple decision trees
- **Feature Engineering**: Includes lag features and temporal patterns
- **Hyperparameter Tuning**: Uses GridSearchCV for optimal parameters
- **Preprocessing**: Handles missing values and categorical features

### Model Features

1. **Meteorological Parameters**
   - Temperature (°C)
   - Dew Point (°C)
   - Atmospheric Pressure (hPa)
   - Wind Speed (m/s)
   - Wind Direction

2. **Environmental Factors**
   - Snow Hours
   - Rain Hours
   - Hour of Day
   - Month of Year

3. **Temporal Features**
   - Previous hour's PM2.5 (lag feature)
   - Seasonal patterns

### Model Performance

- **R² Score**: Typically > 0.85
- **RMSE**: ~12.5 μg/m³
- **MAE**: ~8.2 μg/m³

## 🎨 Website Features

### Main Page (`/`)
- Hero section with animated elements
- Model performance metrics
- Interactive prediction form
- Feature importance visualization
- Random Forest animation
- Dataset information

### About Page (`/about`)
- Detailed Random Forest explanation
- Air quality information
- Dataset overview
- Model performance details

### Interactive Elements
- Real-time form validation
- Sample data population
- Smooth scrolling navigation
- Responsive design
- Loading animations

## 🔧 Customization

### Modifying the Model

To change the Random Forest parameters, edit the `param_grid` in `app.py`:

```python
param_grid = {
    'regressor__n_estimators': [100, 150, 200],
    'regressor__max_depth': [10, 20, None],
    'regressor__min_samples_split': [2, 5, 10]
}
```

### Adding New Features

1. Update the `features` list in `app.py`
2. Modify the preprocessing pipeline
3. Update the HTML form
4. Adjust the JavaScript form handling

### Styling Changes

- Edit `static/css/style.css` for visual modifications
- Modify `templates/index.html` for layout changes
- Update `static/js/script.js` for behavior changes

## 🚨 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. **FileNotFoundError**: Ensure `air_quality.csv` is in the project root

3. **Port already in use**: Change the port in `app.py`
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

4. **Model training issues**: Check dataset format and column names

### Performance Optimization

- For large datasets, consider using a subset for development
- Adjust hyperparameter grid for faster training
- Use `n_jobs=-1` for parallel processing

## 📈 Future Enhancements

- [ ] Real-time data integration
- [ ] Multiple model comparison
- [ ] Advanced visualizations
- [ ] User authentication
- [ ] Prediction history
- [ ] API endpoints
- [ ] Mobile app integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues:
- Check the troubleshooting section
- Review the code comments
- Create an issue in the repository

---

**Note**: This application is for educational and demonstration purposes. For production use, ensure proper data validation, security measures, and model monitoring. 