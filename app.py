from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session storage

# Define the uploads folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Helper function to apply data cleaning operations
def apply_data_cleaning(data, action, column_name=None):
    if action == 'remove_missing_rows':
        data = data.dropna()
    elif action == 'remove_missing_columns':
        data = data.dropna(axis=1)
    elif action == 'fill_forward':
        data = data.fillna(method='ffill')
    elif action == 'fill_backward':
        data = data.fillna(method='bfill')
    elif action == 'interpolate':
        data = data.interpolate()
    elif action == 'remove_duplicates':
        data = data.drop_duplicates()
    elif action == 'uppercase':
        data = data.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    elif action == 'lowercase':
        data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    elif action == 'capitalize':
        data = data.applymap(lambda x: x.capitalize() if isinstance(x, str) else x)
    elif action == 'remove_column' and column_name:
        data = data.drop(columns=[column_name], errors='ignore')
    return data

@app.route('/', methods=['GET', 'POST'])
def landingPage():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.csv'):
            flash("Please upload a valid CSV file.", "error")
            return redirect(request.url)
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        session['file_path'] = file_path
        return redirect(url_for('cleaning'))
    return render_template('landing-page.html')

@app.route('/data-cleaning', methods=['GET', 'POST'])
def cleaning():
    file_path = session.get('file_path')
    if not file_path or not os.path.exists(file_path):
        return 'No file to display', 400

    data = pd.read_csv(file_path)
    if request.method == 'POST':
        action = request.form.get('action')
        column_name = request.form.get('column_name')

        if action:
            cleaned_data = apply_data_cleaning(data, action, column_name)
            cleaned_file_path = os.path.join(UPLOAD_FOLDER, f"cleaned_{os.path.basename(file_path)}")
            cleaned_data.to_csv(cleaned_file_path, index=False)
            session['file_path'] = cleaned_file_path
            flash(f"Data cleaned with action: {action}", "success")
            data = cleaned_data

    table_html = data.to_html(classes='table table-striped', index=False)
    return render_template('data-cleaning.html', table_html=table_html)

@app.route('/visualize/<file_path>', methods=['GET'])
def visualize(file_path):
    full_file_path = os.path.join(UPLOAD_FOLDER, file_path)
    if not os.path.exists(full_file_path):
        flash("File not found.", "error")
        return redirect(url_for('cleaning'))

    try:
        cleaned_data = pd.read_csv(full_file_path)
        chart_data = {
            "columns": cleaned_data.columns.tolist(),
            "data": {col: cleaned_data[col].tolist() for col in cleaned_data.columns}
        }
        return render_template(
            'visualization.html',
            chart_data=json.dumps(chart_data)
        )
    except Exception as e:
        flash(f"Error loading data: {e}", "error")
        return redirect(url_for('cleaning'))
    
# @app.route('/sign-in', methods=['POST'])
# def signin():
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         # Sign in with Firebase
#         user = auth.get_user_by_email(email)
#         # You can add password verification here
#         return jsonify({'success': True, 'uid': user.uid})

#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)})

# @app.route('/sign-up', methods=['POST'])
# def signup():
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         # Create a new user in Firebase Authentication
#         user = auth.create_user(email=email, password=password)
#         return jsonify({'success': True, 'uid': user.uid})

#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)})

@app.route('/home')
def home():
    # Create some dummy data
    dummy_files = [
        {
            'filename': 'report1.pdf',
            'type': 'CSV',
            'path': '/documents/report1.csv',
            'timestamp': '2024-03-15 10:30:00'
        },
        {
            'filename': 'analysis.docx',
            'type': 'CSV',
            'path': '/documents/analysis.csv',
            'timestamp': '2024-03-14 15:45:00'
        },
        {
            'filename': 'spreadsheet.xlsx',
            'type': 'Excel',
            'path': '/documents/spreadsheet.xlsx',
            'timestamp': '2024-03-13 09:15:00'
        }
    ]
    
    return render_template('home.html', files=dummy_files)

@app.route('/create-new')
def create():
    return render_template('create-new.html')

@app.route('/manual-entry')
def manual():
    return render_template('manual.html')

@app.route('/browse-file')
def browseFile():
    return render_template('browse-file.html')

@app.route('/account-setting')
def accountSetting():
    return render_template('account-setting.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/manual-entry', methods=['GET'])
def manual_entry():
    return render_template('manual_entry.html')


if __name__ == "__main__":
    app.run(debug=True)
