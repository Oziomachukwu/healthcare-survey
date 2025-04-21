from flask import Flask, render_template, request, redirect, url_for, Response, send_file
from pymongo import MongoClient
from dotenv import load_dotenv
from User import User
import os
import csv
from io import BytesIO, StringIO
import zipfile


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# MongoDB Connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client.healthcare_survey

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Process form data using User class
            user_data = {
                'age': int(request.form['age']),
                'gender': request.form['gender'],
                'income': float(request.form['income']),
                'expenses': {
                    'utilities': float(request.form.get('utilities', 0)),
                    'entertainment': float(request.form.get('entertainment', 0)),
                    'school_fees': float(request.form.get('school_fees', 0)),
                    'shopping': float(request.form.get('shopping', 0)),
                    'healthcare': float(request.form.get('healthcare', 0))
                }
            }
            
            # Validate and store using User class
            user = User(user_data)
            db.users.insert_one(user.__dict__)
            
            return redirect(url_for('thank_you'))
        except Exception as e:
            return str(e), 400
    return render_template('index.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/admin')
def admin_dashboard():
    # Basic authentication

    # Check if the request has authorization header
    auth = request.authorization
    print("Expected user:", os.getenv('ADMIN_USER'))  # Debug line
    print("Expected pass:", os.getenv('ADMIN_PASS'))  # Debug line
    print("Received auth:", auth)  # Debug line
    
    # If no auth or incorrect credentials, return 401
    if not auth or \
        auth.username != os.getenv('ADMIN_USER') or \
        auth.password != os.getenv('ADMIN_PASS'):
        return Response(
            'Admin Access Required', 401,
            {'WWW-Authenticate': 'Basic realm="Admin Credentials Required"'})
    return render_template('admin.html')

@app.route('/admin/download-csv')
def download_csv():
    try:
        # Query all users from MongoDB
        users = db.users.find()
        
        # Create in-memory CSV
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        
        # Write header
        writer.writerow(User.csv_header())
        
        # Write user data
        for user in users:
            user_obj = User(user)
            writer.writerow(user_obj.to_csv_row())
        
        csv_buffer.seek(0)
        
        return send_file(
            BytesIO(csv_buffer.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='healthcare_data.csv'
        )
    except Exception as e:
        return str(e), 500

@app.route('/admin/download-charts')
def download_charts():
    try:
        # Create in-memory ZIP file
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            # Add all charts from static/charts
            for root, dirs, files in os.walk('static/charts'):
                for file in files:
                    zf.write(os.path.join(root, file))
        
        memory_file.seek(0)
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='healthcare_charts.zip'
        )
    except Exception as e:
        return str(e), 500
    
# Route to serve charts
@app.context_processor
def utility_processor():
    def charts_exists(filename):
        return os.path.exists(os.path.join('static', 'charts', filename))
    return dict(charts_exists=charts_exists)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
