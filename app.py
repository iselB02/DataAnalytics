from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import os
import tempfile
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session storage

# SQLite Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_db.db'  # SQLite database file in the current directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary overhead
db = SQLAlchemy(app)

# Define a simple model for storing file metadata in SQLite
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_url = db.Column(db.String(100), nullable=False)
    user_uid = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Initialize DB manually here
def init_db():
    with app.app_context():
        db.create_all()  # Create the tables if they do not exist already

init_db()  # Call it here


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
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and file.filename.endswith('.csv'):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
            file.save(temp_file.name)
            session['temp_file'] = temp_file.name
            return redirect(url_for('cleaning'))
    return render_template('landing-page.html')

@app.route('/data-cleaning', methods=['GET', 'POST'])
def cleaning():
    temp_file_path = session.get('temp_file')
    if not temp_file_path or not os.path.exists(temp_file_path):
        return 'No file to display', 400

    data = pd.read_csv(temp_file_path)
    
    if request.method == 'POST':
        action = request.form.get('action')
        column_name = request.form.get('column_name')
        
        if action:
            cleaned_data = apply_data_cleaning(data, action, column_name)
            cleaned_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
            cleaned_data.to_csv(cleaned_filename.name, index=False)
            session['temp_file'] = cleaned_filename.name
            flash(f'Data cleaned with action: {action}', 'success')
            data = cleaned_data

    table_html = data.to_html(classes='table table-striped', index=False)
    return render_template('data-cleaning.html', table_html=table_html)

@app.route('/save-to-db', methods=['POST'])
def save_to_db():
    temp_file_path = session.get('temp_file')
    if not temp_file_path or not os.path.exists(temp_file_path):
        return jsonify({'success': False, 'message': 'No cleaned file to save'})

    try:
        # Retrieve the UID from the request
        uid = request.json.get('uid')
        if not uid:
            return jsonify({'success': False, 'message': 'UID is required'})

        # Verify the UID using Firebase Authentication
        user = auth.get_user(uid)

        # Upload file to Firebase Storage
        blob = storage.bucket().blob(f'cleaned_data/{os.path.basename(temp_file_path)}')
        blob.upload_from_filename(temp_file_path)
        file_url = blob.public_url

        # Save file metadata to SQLite
        metadata = File(
            filename=os.path.basename(temp_file_path),
            file_url=file_url,
            user_uid=user.uid
        )
        db.session.add(metadata)
        db.session.commit()

        return jsonify({'success': True, 'message': 'File saved to database', 'file_url': file_url})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/visualize', methods=['POST'])
def visualize_and_save():
    # Ensure the cleaned file is available
    temp_file_path = session.get('temp_file')
    if not temp_file_path or not os.path.exists(temp_file_path):
        return 'No file to display', 400
    
    data = pd.read_csv(temp_file_path)

    # Visualize data (you can add a visualization logic here)
    # For now, let's just show the cleaned data as HTML table in the frontend
    table_html = data.to_html(classes='table table-striped', index=False)

    # Save the cleaned data into the database
    # Convert the cleaned DataFrame to a CSV binary format
    cleaned_csv = data.to_csv(index=False).encode('utf-8')
    cleaned_data_entry = CleanedData(
        filename=os.path.basename(temp_file_path),
        cleaned_data=cleaned_csv
    )
    db.session.add(cleaned_data_entry)
    db.session.commit()

    flash('Data has been visualized and saved successfully!', 'success')
    
    return jsonify({'table_html': table_html, 'filename': os.path.basename(temp_file_path)})

@app.route('/sign-in', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    try:
        # Sign in with Firebase
        user = auth.get_user_by_email(email)
        # You can add password verification here
        return jsonify({'success': True, 'uid': user.uid})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/sign-up', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']

    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user(email=email, password=password)
        return jsonify({'success': True, 'uid': user.uid})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/home')
def home():
    return render_template('home.html')

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
