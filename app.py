from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file, jsonify
import os
import pandas as pd
import json
import google.generativeai as genai
import datetime
import numpy as np


genai.configure(api_key='AIzaSyAs7TiLmL-JRwRbkHo0vLC1P6XnR-P5w3Y')
model = genai.GenerativeModel('gemini-1.5-flash')
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session storage


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


# Register the filter with Jinja2
app.jinja_env.filters['format_date'] = format_date

# Helper function to clean missing data based on mean, median, or mode
def clean_missing_data(df):
    for column in df.columns:
        if df[column].dtype == 'object':  # Categorical column
            mode_value = df[column].mode()[0]  # Fill with mode (most frequent value)
            df[column].fillna(mode_value, inplace=True)
        else:  # Numerical column
            skewness = df[column].skew()
            if np.abs(skewness) < 0.5:
                mean_value = df[column].mean()  # Fill with mean for roughly normal distributions
                df[column].fillna(mean_value, inplace=True)
            else:
                median_value = df[column].median()  # Fill with median for skewed distributions
                df[column].fillna(median_value, inplace=True)
    return df

# Define the uploads and JSON folders
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
JSON_FOLDER = os.path.join(os.path.dirname(__file__), 'json_data')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(JSON_FOLDER):
    os.makedirs(JSON_FOLDER)

@app.route('/explain', methods=['POST'])
def explain_data():
    # Example: Request for explanation of the chart data or some result
    data_to_explain = request.json.get('data')  # Get the data to explain (from frontend)

    # Start a new chat with the AI model
    chat = model.start_chat(history=[])

    # Sending the message to explain the data
    prompt = f"Explain the following data analysis: {data_to_explain}"
    response = chat.send_message(prompt)

    # Return the explanation to the frontend
    return jsonify({'explanation': response.text})

@app.route('/generate-report', methods=['POST'])
def generate_report():
    # Get the chart image, chart data, and the prompt
    data = request.json
    chart_image = data.get('chart_image')  # This is the base64 image
    prompt = data.get('prompt')
    chart_data = data.get('chart_data')  # Chart data to help with report generation

    # Create the prompt for Gemini using the provided data
    prompt_message = f"{prompt}\nHere is the chart data:\n{chart_data}"

    # Start the chat session with Gemini and send the prompt
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt_message)  # Send the prompt message to Gemini
    
    # You can optionally include the chart image as part of the conversation
    # Depending on Gemini's capabilities, you may pass the image or process it further
    
    return jsonify({'report': response.text})


# Function to convert CSV to JSON
def csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path)
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
        if not file or not file.filename.endswith('.csv'):
            flash("Please upload a valid CSV file.", "error")
            return redirect(url_for('home'))

        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
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
        for file in os.listdir(UPLOAD_FOLDER) if file.endswith('.csv')
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

        # Save CSV file
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"manual_entry_{timestamp}.csv"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pd.DataFrame(rows, columns=columns).to_csv(file_path, index=False)

        # Update session for data cleaning
        session['file_path'] = file_path

        return jsonify({
            "success": True,
            "message": f"CSV saved as {filename}. Redirecting to Data Cleaning.",
            "redirect_url": url_for('cleaning')  # Ensure this generates the correct URL
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



@app.route('/cleaning', methods=['GET', 'POST'])
def cleaning():
    if request.method == 'POST' and request.form.get('action') == 'clean_data':
        file_path = session.get('file_path')
        if not file_path:
            flash("No file uploaded", "error")
            return redirect(url_for('home'))

        # Read the CSV file into DataFrame
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            flash(f"Error reading CSV file: {e}", "error")
            return redirect(url_for('home'))

        # Clean missing data using the helper function
        df = clean_missing_data(df)

        # Save cleaned DataFrame with the same name but with "_cleaned" suffix
        original_filename = os.path.basename(file_path)
        cleaned_filename = f"{os.path.splitext(original_filename)[0]}_cleaned.csv"
        cleaned_file_path = os.path.join(UPLOAD_FOLDER, cleaned_filename)

        try:
            df.to_csv(cleaned_file_path, index=False)
        except Exception as e:
            flash(f"Error saving cleaned CSV file: {e}", "error")
            return redirect(url_for('home'))

        # Convert cleaned CSV to JSON and save
        try:
            json_file_path = csv_to_json(cleaned_file_path)
            session['json_file_path'] = json_file_path
        except Exception as e:
            flash(f"Error converting CSV to JSON: {e}", "error")
            return redirect(url_for('cleaning'))

        # Optionally, update 'file_path' to point to the cleaned file
        session['file_path'] = cleaned_file_path

        flash(f"Missing data cleaned successfully. Saved as {cleaned_filename}.", "success")
        return render_template('data-cleaning.html', table_html=df.to_html(classes='table table-striped'))

    # Handle GET request
    file_path = session.get('file_path')
    if not file_path:
        return render_template('data-cleaning.html', table_html=None)

    # Read the CSV file into DataFrame to display
    try:
        df = pd.read_csv(file_path)
        table_html = df.to_html(classes='table table-striped')
    except Exception as e:
        flash(f"Error reading CSV file: {e}", "error")
        table_html = None

    return render_template('data-cleaning.html', table_html=table_html)


# Route: Save to Visualize
@app.route('/save-to-visualize', methods=['POST'])
def save_to_visualize():
    # Redirect to visualize after ensuring cleaned data exists
    json_file_path = session.get('json_file_path')
    if not json_file_path or not os.path.exists(json_file_path):
        flash("No JSON file found. Please clean data first.", "error")
        return redirect(url_for('cleaning'))
    return redirect(url_for('visualize'))

@app.route('/visualize', methods=['GET'])
def visualize():
    json_file_path = session.get('json_file_path')
    
    # Check if the file exists
    if not json_file_path or not os.path.exists(json_file_path):
        flash("No JSON file found. Please clean data first.", "error")
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
        for file in uploaded_files if file.endswith(('.csv', '.xlsx'))  # Filter by allowed file types
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