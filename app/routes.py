import requests
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash
from app import app, db, celery
from .models import Results, Tasks
from .forms import WebsiteForm


@celery.task
def parse_website_text(_id):
    """Background task to send requests to a webiste and counting occurance of word Python."""
    task = Tasks.query.get(_id)
    task.task_status = 'PENDING'
    db.session.commit()
    address = task.address
    if not (address.startswith('http') and  address.startswith('https')):
        address = 'http://' + address
    with app.app_context():
        res = requests.get(address) 
        words_count=0
        if res.ok:
            words = res.text.split()
            words_count = words.count("Python")
            
        result = Results(address=address, words_count=words_count, http_status_code=res.status_code)
        task = Tasks.query.get(_id)
        task.task_status = 'FINISHED'
        db.session.add(result)
        db.session.commit()


@app.route('/', methods=['POST', 'GET'])
@app.route('/add_website', methods=['POST', 'GET'])
def website():
    website_form = WebsiteForm()
    if request.method == 'POST':
        if website_form.validate_on_submit():
            address = request.form.get('address')
            task = Tasks(address=address, timestamp=datetime.now(), task_status='NOT_STARTED')
            db.session.add(task)
            db.session.commit()
            parse_website_text.delay(task._id)
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=website_form,error = error)
    return render_template('add_website.html', form=website_form)


@app.route('/results')
def get_results():
    results = Results.query.all()
    return render_template('results.html', results=results)