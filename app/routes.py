from flask import Flask, render_template, request, redirect, url_for, Response, send_file
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import csv
from io import BytesIO
import zipfile

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# MongoDB Setup
client = MongoClient(os.getenv('MONGO_URI'))
db = client.healthcare_survey

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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
        db.users.insert_one(user_data)
        update_csv()
        return redirect(url_for('thank_you'))
    return render_template('index.html')

def update_csv():
    users = db.users.find()
    with open('../data/survey_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Age','Gender','Income','Utilities',
                        'Entertainment','School Fees','Shopping','Healthcare'])
        for user in users:
            writer.writerow([
                user['age'],
                user['gender'],
                user['income'],
                user['expenses']['utilities'],
                user['expenses']['entertainment'],
                user['expenses']['school_fees'],
                user['expenses']['shopping'],
                user['expenses']['healthcare']
            ])

@app.route('/admin')
def admin_dashboard():
    auth = request.authorization
    if not auth or auth.username != os.getenv('ADMIN_USER') or auth.password != os.getenv('ADMIN_PASS'):
        return Response(
            'Login Required', 401,
            {'WWW-Authenticate': 'Basic realm="Admin Access Required"'})
    return render_template('admin.html')

@app.route('/download-charts')
def download_charts():
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in os.listdir('static/charts'):
            zf.write(f'static/charts/{file}')
    memory_file.seek(0)
    return send_file(memory_file, mimetype='application/zip',
                   download_name='healthcare_charts.zip')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)