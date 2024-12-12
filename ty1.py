import pandas as pd
import numpy as np
import re

def analyze_data(df):
    """
    Analyzes the given data for duplicates, missing values, outliers, and wrong formats.
    Data is expected to be a DataFrame.
    Returns a dictionary with counts.
    """
    if not isinstance(df, pd.DataFrame) or df.empty:
        return {"error": "No valid data provided to analyze."}

    analysis = {
        'duplicates': 0,
        'missing': {},
        'outliers': {},
        'wrongFormat': {}
    }

    # Helper functions
    def is_numeric(val):
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False

    # Sample format validator (email)
    def is_valid_email(val):
        if val is None or val == '':
            return True  # Missing is handled separately, here we just check format
        pattern = r"^\S+@\S+\.\S+$"
        return bool(re.match(pattern, str(val)))

    # Analyze duplicates (entire row duplicates)
    analysis['duplicates'] = df.duplicated().sum()  # Count duplicate rows

    # Analyze missing values
    for col in df.columns:
        missing_count = df[col].isnull().sum()  # Count missing values (NaN)
        if missing_count > 0:
            analysis['missing'][col] = missing_count

    # Detect outliers (for numeric columns)
    for col in df.columns:
        if df[col].dtype in [np.float64, np.int64]:  # Only check for numeric columns
            numeric_values = df[col].dropna()
            if len(numeric_values) > 1:  # Ensure we have enough data points
                q1 = numeric_values.quantile(0.25)
                q3 = numeric_values.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Print values for debugging
                print(f"Column: {col}")
                print(f"Q1: {q1}, Q3: {q3}, IQR: {iqr}")
                print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
                
                outliers = numeric_values[(numeric_values < lower_bound) | (numeric_values > upper_bound)]
                outlier_count = len(outliers)
                print(f"Outliers: {outliers}")
                
                if outlier_count > 0:
                    analysis['outliers'][col] = outlier_count


    # Wrong format: For demonstration, check email columns
    for col in df.columns:
        if 'email' in col.lower():
            invalid_count = df[col].apply(lambda x: not is_valid_email(x)).sum()
            if invalid_count > 0:
                analysis['wrongFormat'][col] = invalid_count

    return analysis

# Load CSV (replace with your actual file path)
df = pd.read_csv('laptopData.csv')

# Run the analysis function
analysis_results = analyze_data(df)

# Print the results
print("Analysis Results:", analysis_results)

# Display results in a readable format
print("\nSummary of Duplicates (rows):")
print(f"Duplicate Rows: {analysis_results['duplicates']}")

print("\nSummary of Missing Values:")
print(analysis_results['missing'])

print("\nSummary of Outliers:")
print(analysis_results['outliers'])

print("\nSummary of Wrong Formats:")
print(analysis_results['wrongFormat'])