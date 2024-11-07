from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn.neighbors import NearestNeighbors
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
db = SQLAlchemy(app)

# Job Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)

# Endpoint to add a job
@app.route('/add-job', methods=['POST'])
def add_job():
    data = request.json
    new_job = Job(title=data['title'], skills=data['skills'])
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'message': 'Job added!'}), 201

# Endpoint to match jobs
@app.route('/match-jobs/<int:user_id>', methods=['GET'])
def match_jobs(user_id):
    user = User.query.get(user_id)
    jobs = Job.query.all()

    user_skills = user.skills.split(',')
    job_data = [(job.id, job.title, job.skills.split(',')) for job in jobs]
    
    # Create a DataFrame for matching
    df = pd.DataFrame(job_data, columns=['id', 'title', 'skills'])
    
    # Matching Logic
    model = NearestNeighbors(metric='cosine')
    model.fit(df['skills'].apply(lambda x: [skill.strip() for skill in x]).tolist())
    distances, indices = model.kneighbors([user_skills], n_neighbors=3)

    matched_jobs = df.iloc[indices[0]].to_dict(orient='records')
    
    return jsonify(matched_jobs)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
