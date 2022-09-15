from flask import Flask, render_template, session, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret:3'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def index(): 
    survey = surveys["satisfaction"]
    return render_template('root.html', survey=survey)

@app.route('/questions/<int:question_num>')
def show_question(question_num):
    responses = session["responses"]

    if(responses == None):
        return redirect('/')

    if(len(responses) != question_num):
        flash(f"Invalid question number {question_num}")
        return redirect(f"/questions/{len(responses)}")

    if(len(responses) == len(surveys["satisfaction"].questions)):
        return redirect('/completesurvey')
    
    question = surveys["satisfaction"].questions[question_num]
    return render_template("question.html", question_num=question_num, question=question) 


@app.route('/startsurvey', methods=["POST"])
def start_survey():
    session["responses"] = []
    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def get_answer():
    answer = request.form['answer']
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    
    if(len(responses) == len(surveys["satisfaction"].questions)):
        return redirect('/completesurvey')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/completesurvey')
def complete():
    return render_template('complete.html')
