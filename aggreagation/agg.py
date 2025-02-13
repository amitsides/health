import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Collection and Preparation
def get_health_metrics():
    # Connect to your database and fetch data
    query = """
    SELECT 
        p.UserID,
        p.Date,
        p.StepCount,
        p.CaloriesBurned,
        p.HeartRate,
        b.GlucoseLevel,
        b.Cholesterol
    FROM PhysicalActivity p
    JOIN BloodTests b 
    ON p.UserID = b.UserID AND p.Date = b.Date
    WHERE p.StepCount IS NOT NULL 
    AND p.CaloriesBurned IS NOT NULL 
    AND p.HeartRate IS NOT NULL
    AND b.GlucoseLevel IS NOT NULL
    AND b.Cholesterol IS NOT NULL
    """
    
    # For demonstration, creating sample data
    np.random.seed(42)
    n_samples = 1000
    
    df = pd.DataFrame({
        'UserID': np.random.randint(1, 101, n_samples),
        'Date': pd.date_range(start='2023-01-01', periods=n_samples),
        'StepCount': np.random.normal(8000, 2000, n_samples),
        'CaloriesBurned': np.random.normal(2000, 500, n_samples),
        'HeartRate': np.random.normal(75, 10, n_samples),
        'GlucoseLevel': np.random.normal(100, 15, n_samples),
        'Cholesterol': np.random.normal(180, 30, n_samples)
    })
    
    return df

# 2. Data Analysis and Preprocessing
def analyze_health_data(df):
    # Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())
    
    # Correlation analysis
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix of Health Metrics')
    plt.tight_layout()
    plt.show()
    
    # Distribution plots
    metrics = ['StepCount', 'CaloriesBurned', 'HeartRate', 'GlucoseLevel', 'Cholesterol']
    plt.figure(figsize=(15, 10))
    for i, metric in enumerate(metrics, 1):
        plt.subplot(2, 3, i)
        sns.histplot(df[metric], kde=True)
        plt.title(f'{metric} Distribution')
    plt.tight_layout()
    plt.show()
    
    return df

# 3. Feature Engineering
def prepare_features(df):
    # Add time-based features
    df['DayOfWeek'] = pd.to_datetime(df['Date']).dt.dayofweek
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    
    # Calculate moving averages
    df['StepCount_MA7'] = df.groupby('UserID')['StepCount'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean())
    df['CaloriesBurned_MA7'] = df.groupby('UserID')['CaloriesBurned'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean())
    
    # Create feature matrix
    feature_columns = [
        'StepCount', 'CaloriesBurned', 'HeartRate', 
        'DayOfWeek', 'Month', 'StepCount_MA7', 'CaloriesBurned_MA7'
    ]
    
    return df, feature_columns

# 4. Model Training and Evaluation
def train_health_models(df, feature_columns):
    # Prepare targets
    targets = ['GlucoseLevel', 'Cholesterol']
    models = {}
    results = {}
    
    for target in targets:
        X = df[feature_columns]
        y = df[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Store results
        models[target] = {
            'model': model,
            'scaler': scaler,
            'feature_importance': dict(zip(feature_columns, 
                                        model.feature_importances_))
        }
        
        results[target] = {
            'mse': mse,
            'r2': r2,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        # Plot feature importance
        plt.figure(figsize=(10, 6))
        importances = pd.Series(model.feature_importances_, index=feature_columns)
        importances.sort_values().plot(kind='barh')
        plt.title(f'Feature Importance for {target}')
        plt.tight_layout()
        plt.show()
        
        # Plot predictions vs actual
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title(f'{target} - Actual vs Predicted')
        plt.tight_layout()
        plt.show()
        
    return models, results

# 5. Main execution
def main():
    # Get data
    df = get_health_metrics()
    
    # Analyze data
    df = analyze_health_data(df)
    
    # Prepare features
    df, feature_columns = prepare_features(df)
    
    # Train models and get results
    models, results = train_health_models(df, feature_columns)
    
    # Print results
    for target, metrics in results.items():
        print(f"\nResults for {target}:")
        print(f"Mean Squared Error: {metrics['mse']:.2f}")
        print(f"R² Score: {metrics['r2']:.2f}")

if __name__ == "__main__":
    main()