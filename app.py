from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import os
import pandas as pd
import json
import google.generativeai as genai
import datetime
import numpy as np
import uuid
import re
from collections import Counter
import time

# ⚠️ Security Warning: Ensure you have revoked the exposed API key before proceeding.
genai.configure(api_key='YOUR_NEW_SECURE_API_KEY')  # Replace with your new secure API key
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'  # Replace with a secure secret key

# Configuration for display preferences
DISPLAY_DETAILS = {
    'duplicates': True,       # Show per-column counts
    'missing': False,         # Show only total count
    'outliers': False,        # Show only total count
    'wrongFormat': True       # Show per-column counts
}

# Define the uploads and JSON folders
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
JSON_FOLDER = os.path.join(os.path.dirname(__file__), 'json_data')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(JSON_FOLDER):
    os.makedirs(JSON_FOLDER)

# Register the filter with Jinja2
def format_date(value, date_format='%Y-%m-%d'):
    from datetime import datetime
    if isinstance(value, (int, float)):
        # Convert Unix timestamp (float/int) to datetime
        value = datetime.fromtimestamp(value)
    if isinstance(value, datetime):
        return value.strftime(date_format)
    if isinstance(value, str):
        try:
            # Attempt to parse string format
            parsed_date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return parsed_date.strftime(date_format)
        except ValueError:
            return value  # Return value as-is if parsing fails
    return value  # Return value as-is if unsupported type

app.jinja_env.filters['format_date'] = format_date




def clean_and_handle_outliers(df):
    """
    This function cleans the dataframe by:
    - Removing one row of each duplicated row.
    - Filling missing values in categorical columns with the mode.
    - Handling outliers based on skewness (mean for normal, median for skewed).
    - Outliers are replaced by the mean or median depending on the column's distribution.
    """
    # Remove duplicate rows (keeps the first occurrence)
    df.drop_duplicates(inplace=True)

    for column in df.columns:
        if df[column].dtype == 'object':  # Categorical column
            mode_value = df[column].mode()[0]  # Fill with mode (most frequent value)
            df[column].fillna(mode_value, inplace=True)
        else:  # Numerical column
            # Compute IQR and detect outliers
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Identify outliers
            outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
            
            # Handle outliers based on skewness
            skewness = df[column].skew()
            if np.abs(skewness) < 0.5:  # Normal distribution
                df.loc[outliers, column] = df[column].mean()  # Replace outliers with mean
            else:  # Skewed distribution
                df.loc[outliers, column] = df[column].median()  # Replace outliers with median

            # Fill remaining missing values based on skewness
            if np.abs(skewness) < 0.5:
                mean_value = df[column].mean()  # Use mean for normal distributions
                df[column].fillna(mean_value, inplace=True)
            else:
                median_value = df[column].median()  # Use median for skewed distributions
                df[column].fillna(median_value, inplace=True)
                

    return df


import numpy as np
import re
from collections import Counter

def analyze_data(data):
    """
    Analyzes the given data for duplicates, missing values, outliers, and wrong formats.
    Data is expected to be a list of dictionaries, each representing a row.
    Returns a dictionary with counts.
    """
    if not isinstance(data, list) or len(data) == 0 or not all(isinstance(row, dict) for row in data):
        return {"error": "No valid data provided to analyze."}

    columns = data[0].keys()
    analysis = {
        'duplicates': [],
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

    # Count duplicates by row
    rows = [tuple(row.items()) for row in data]  # Convert rows into tuples of key-value pairs
    row_counts = Counter(rows)
    
    # Get duplicate rows
    duplicate_rows = [dict(row) for row, count in row_counts.items() if count > 1]

    if duplicate_rows:
        for row in duplicate_rows:
            duplicate_count = row_counts[tuple(row.items())]
            analysis['duplicates'].append({'row': row, 'count': duplicate_count})

    # Analyze each column
    for col in columns:
        values = [row[col] for row in data]
        
        # Count missing data (None and NaN values)
        missing_count = sum(1 for val in values if val is None or (isinstance(val, float) and np.isnan(val)))
        if missing_count > 0:
            analysis['missing'][col] = missing_count

        col_values = [row[col] for row in data]  # Extract column values for outlier detection
        if isinstance(col_values[0], (int, float)):  # Only check for numeric columns
            numeric_values = [val for val in col_values if isinstance(val, (int, float)) and not np.isnan(val)]
            
            # Debugging: Check the numeric values
            print(f"Column: {col} - Numeric Values: {numeric_values}")
            
            if len(numeric_values) > 1:  # Ensure we have enough data points
                q1 = np.percentile(numeric_values, 25)
                q3 = np.percentile(numeric_values, 75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Debugging: Check bounds
                print(f"Column: {col} - Q1: {q1}, Q3: {q3}, IQR: {iqr}, Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
                
                outlier_count = sum(1 for v in numeric_values if v < lower_bound or v > upper_bound)
                
                # Debugging: Check outlier count
                print(f"Column: {col} - Outlier Count: {outlier_count}")
                
                if outlier_count > 0:
                    analysis['outliers'][col] = outlier_count

        # Wrong format: For demonstration, check email columns
        if 'email' in col.lower():
            invalid_count = sum(1 for val in values if not is_valid_email(val))
            # Exclude missing because it's already counted in 'missing'
            if invalid_count > 0:
                analysis['wrongFormat'][col] = invalid_count

    # Summarize missing values (total missing count for each column)
    total_missing_values = {col: analysis['missing'].get(col, 0) for col in columns}
    analysis['totalMissing'] = sum(total_missing_values.values())  # Total missing values across all columns

    return analysis




# Function to convert CSV to JSON
def csv_to_json(csv_file_path):
    # Ensure that empty strings are treated as NaN
    df = pd.read_csv(csv_file_path, na_values=[''])
    json_data = {
        "columns": df.columns.tolist(),
        "data": df.to_dict(orient='records')  # Each row as a dictionary
    }
    json_file_path = os.path.join(JSON_FOLDER, os.path.basename(csv_file_path).replace('.csv', '.json'))
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    return json_file_path

# Route: Home (File Upload)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("No file part in the request.", "danger")
            return redirect(url_for('home'))
        if file.filename == '':
            flash("No file selected for uploading.", "danger")
            return redirect(url_for('home'))
        if not file.filename.lower().endswith('.csv'):
            flash("Please upload a valid CSV file.", "danger")
            return redirect(url_for('home'))

        # Generate a unique filename to prevent overwriting
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        try:
            # Ensure that empty strings are treated as NaN during CSV parsing
            df = pd.read_csv(file, na_values=[''])
            df.to_csv(file_path, index=False)  # Save the cleaned CSV
        except Exception as e:
            flash(f"Failed to save file: {e}", "danger")
            return redirect(url_for('home'))
        session['file_path'] = file_path

        flash("File uploaded successfully. Redirecting to Data Cleaning.", "success")
        return redirect(url_for('cleaning'))

    # Optionally, display a list of uploaded files
    uploaded_files = [
        {
            'filename': file,
            'path': os.path.join(UPLOAD_FOLDER, file),
            'type': os.path.splitext(file)[1].lstrip('.').upper(),
            'timestamp': datetime.datetime.fromtimestamp(
                os.path.getmtime(os.path.join(UPLOAD_FOLDER, file))
            ).strftime('%Y-%m-%d %H:%M:%S')
        }
        for file in os.listdir(UPLOAD_FOLDER) if file.lower().endswith('.csv')
    ]

    # Sort by timestamp (newest first) and limit to the top 7
    uploaded_files.sort(key=lambda x: x['timestamp'], reverse=True)
    top_files = uploaded_files[:7]

    return render_template('home.html', files=top_files)

@app.route('/save-csv', methods=['POST'])
def save_csv():
    try:
        # Parse JSON from request
        data = request.get_json()
        columns = data.get('columns', [])
        rows = data.get('data', [])

        # Validate input
        if not columns:
            return jsonify({"error": "No columns provided. Please ensure you set column titles."}), 400
        if not rows or not all(len(row) == len(columns) for row in rows):
            return jsonify({"error": "Invalid or incomplete rows. Ensure all rows match the column count."}), 400

        # Generate a unique filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"manual_entry_{timestamp}_{uuid.uuid4().hex}.csv"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        df = pd.DataFrame(rows, columns=columns)
        # Treat empty strings as NaN
        df.replace('', np.nan, inplace=True)
        df.to_csv(file_path, index=False)

        # Update session for data cleaning
        session['file_path'] = file_path

        return jsonify({
            "success": True,
            "message": f"CSV saved as {unique_filename}. Redirecting to Data Cleaning.",
            "redirect_url": url_for('cleaning')  # Ensure this generates the correct URL
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/cleaning', methods=['GET', 'POST'])
def cleaning():
    def is_data_clean(df):
        """
        Check if the dataset is already clean.
        Returns True if no missing values, no duplicates, no outliers, and no wrong formats.
        """
        # Check for missing values
        if df.isnull().sum().sum() > 0:
            return False

        # Check for duplicates
        if df.duplicated().sum() > 0:
            return False

        # Check for outliers in numeric columns
        for col in df.select_dtypes(include=[np.number]).columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            if outliers > 0:
                return False

        # Check for wrong formats (e.g., invalid emails)
        email_columns = [c for c in df.columns if 'email' in c.lower()]
        email_pattern = r"^\S+@\S+\.\S+$"
        for c in email_columns:
            invalid_emails = df[c].dropna().apply(lambda x: not bool(re.match(email_pattern, str(x))))
            if invalid_emails.sum() > 0:
                return False

        # If none of the checks returned False, the data is considered clean
        return True

    if request.method == 'POST':
        file_path = session.get('file_path')
        if not file_path:
            flash("No file uploaded.", "danger")
            return redirect(url_for('home'))

        # Read the CSV file into DataFrame (ensure empty strings are treated as NaN)
        try:
            df = pd.read_csv(file_path, na_values=[''])
        except Exception as e:
            flash(f"Error reading CSV file: {e}", "danger")
            return redirect(url_for('home'))

        # Analyze the data for duplicates, errors, etc.
        data_records = df.to_dict(orient='records')
        analysis = analyze_data(data_records)  # This should return a dict with counts

        # Check if data is already clean
        if is_data_clean(df):
            flash("The dataset is already clean. No further cleaning required.", "info")
            
            # Convert to JSON and save (in case it wasn't done before)
            try:
                json_file_path = csv_to_json(file_path)
                session['json_file_path'] = json_file_path
            except Exception as e:
                flash(f"Error converting CSV to JSON: {e}", "danger")
                return redirect(url_for('cleaning'))

            return render_template('data-cleaning.html', 
                                   table_html=df.to_html(classes='table table-striped', index=False),
                                   analysis=None,  # No analysis needed
                                   display_details=DISPLAY_DETAILS)
        
        # Data requires cleaning
        flash("Data requires cleaning. Proceeding with cleaning operations.", "warning")

        # Capture the original data before cleaning
        original_df = df.copy()

        # Clean missing data using the helper function
        df = clean_and_handle_outliers(df)

        # Save cleaned DataFrame with "_cleaned" suffix
        original_filename = os.path.basename(file_path)
        cleaned_filename = f"{os.path.splitext(original_filename)[0]}_cleaned.csv"
        cleaned_file_path = os.path.join(UPLOAD_FOLDER, cleaned_filename)

        try:
            df.to_csv(cleaned_file_path, index=False)
            flash(f"Missing data cleaned successfully. Saved as {cleaned_filename}.", "success")
        except Exception as e:
            flash(f"Error saving cleaned CSV file: {e}", "danger")
            return redirect(url_for('home'))

        # Convert cleaned CSV to JSON and save
        try:
            json_file_path = csv_to_json(cleaned_file_path)
            session['json_file_path'] = json_file_path
        except Exception as e:
            flash(f"Error converting CSV to JSON: {e}", "danger")
            return redirect(url_for('cleaning'))

        # Update 'file_path' to point to the cleaned file
        session['file_path'] = cleaned_file_path

        # Analyze the cleaned data
        cleaned_data_records = df.to_dict(orient='records')
        cleaned_analysis = analyze_data(cleaned_data_records)

        return render_template('data-cleaning.html', 
                               original_table_html=original_df.to_html(classes='table table-striped', index=False),
                               cleaned_table_html=df.to_html(classes='table table-striped', index=False),
                               table_html=df.to_html(classes='table table-striped', index=False),
                               analysis=cleaned_analysis,
                               display_details=DISPLAY_DETAILS)

    # Handle GET request
    file_path = session.get('file_path')
    if not file_path:
        return render_template('data-cleaning.html', 
                               table_html=None, 
                               analysis=None,
                               display_details=DISPLAY_DETAILS)

    # Read the CSV file into DataFrame
    try:
        df = pd.read_csv(file_path, na_values=[''])
        table_html = df.to_html(classes='table table-striped', index=False)
    except Exception as e:
        flash(f"Error reading CSV file: {e}", "danger")
        table_html = None

    # Analyze the data
    data_records = df.to_dict(orient='records')
    analysis = analyze_data(data_records)

    # Determine if data is clean
    if is_data_clean(df):
        flash("The dataset is already clean. No further cleaning required.", "info")
        analysis = None  # No analysis needed
    else:
        flash("Data has issues. Please review the analysis below.", "warning")
    time.sleep(6)
    return render_template('data-cleaning.html', 
                           table_html=table_html, 
                           analysis=analysis,
                           display_details=DISPLAY_DETAILS)

@app.route('/save-to-visualize', methods=['POST'])
def save_to_visualize():
    # Redirect to visualize after ensuring cleaned data exists
    json_file_path = session.get('json_file_path')
    if not json_file_path or not os.path.exists(json_file_path):
        flash("No JSON file found. Please clean data first.", "danger")
        return redirect(url_for('cleaning'))
    return redirect(url_for('visualize'))

@app.route('/visualize', methods=['GET'])
def visualize():
    json_file_path = session.get('json_file_path')
    
    # Check if the file exists
    if not json_file_path or not os.path.exists(json_file_path):
        flash("No JSON file found. Please clean data first.", "danger")
        return redirect(url_for('cleaning'))

    # Read the JSON data
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Assuming json_data is structured with 'columns' and 'data' keys, convert to pandas DataFrame
    df = pd.DataFrame(json_data['data'])

    # Prepare the chart data to pass to the template
    chart_data = {
        "columns": list(df.columns),  # Get column names
        "data": df.to_dict(orient='list')  # Convert the DataFrame to a dictionary
    }

    return render_template('visualization.html', chart_data=json.dumps(chart_data))

@app.route('/get-json-data', methods=['GET'])
def get_json_data():
    """Serve JSON data dynamically for visualization."""
    json_file_path = session.get('json_file_path')
    if not json_file_path or not os.path.exists(json_file_path):
        return jsonify({"error": "No JSON data found"}), 404

    with open(json_file_path, 'r') as json_file:
        chart_data = json.load(json_file)

    return jsonify(chart_data)

@app.route('/create-new')
def create():
    return render_template('create-new.html')

@app.route('/manual-entry')
def manual():
    return render_template('manual.html')

@app.route('/browse-file', methods=['GET'])
def browse_files():
    # Get the list of files in the upload folder
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    files = [
        {
            'name': file,
            'path': os.path.join(UPLOAD_FOLDER, file),
            'date_modified': os.path.getmtime(os.path.join(UPLOAD_FOLDER, file)),  # File modification timestamp
            'size': os.path.getsize(os.path.join(UPLOAD_FOLDER, file))  # File size in bytes
        }
        for file in uploaded_files if file.lower().endswith(('.csv', '.xlsx'))  # Filter by allowed file types
    ]

    # Sort files by modification time (most recent first)
    files.sort(key=lambda x: x['date_modified'], reverse=True)

    # Separate into recent (top 5) and history (all files)
    recent_files = files[:5]
    history_files = files

    return render_template('browse-file.html', recent_files=recent_files, history_files=history_files)

@app.route('/view-file/<filename>', methods=['GET'])
def view_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Read the file content
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({"filename": filename, "content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-file/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Delete the file
    try:
        os.remove(file_path)
        return jsonify({"success": True, "message": f"File '{filename}' deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/account-setting')
def accountSetting():
    return render_template('account-setting.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run(debug=True)
