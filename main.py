from flask import request

from flask import Flask, render_template, request
from flask import Flask, flash, render_template, request , session , redirect
from forms import SignInForm, SignUpForm, AddProjectForm
from forms import TaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TPhits'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


@app.route('/')
def main():
    _user_id = session.get('user')
    if _user_id:
        return redirect('/userHome')

    todolist = [
        {
            'name': 'Buy milk',
            'description':'Buy 2 liters of milk in Coopmart.'
        },
        {
            'name':'Get money',
            'description':'Get 500k from ATM'
        }
    ]
    return render_template('index.html', todolist=todolist)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():

    form = SignUpForm()
    if form.validate_on_submit():
        print("Validate on submit")
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        if(db.session.query(models.User).filter_by(email=_email).count() == 0):
            user = models.User(first_name = _fname, last_name = _lname, email = _email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('signUpSuccess.html', user = user)
        else:
            flash('Email {} is already exsits!'.format(_email))
            return render_template('signup.html', form = form)

    # return render_template('signup.html')
    print("Not validate on submit")
    return render_template('signup.html', form = form)



@app.route('/signIn', methods=['GET','POST'])
def signIn():
    form = SignInForm()
    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email = _email).first()
        if(user is None):
            flash('Wrong email address or password!')
        else:
            if(user.check_password(_password)):
                session['user'] = user.user_id
                return redirect('/userHome')
            else:
                flash('Wrong email address or password!')

    return render_template('signin.html', form = form)


@app.route('/userHome', methods=['GET','POST'])
def userhome():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user = user)
    else:
        return redirect('/')


@app.route('/logOut', methods=['GET','POST'])
def logOut():
    session.pop('user',None)
    return redirect('/signIn')


@app.route('/newTask', methods=['GET', 'POST'])
def newTask():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = TaskForm()
        form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
        form.inputProject.choices = [(p.project_id, p.project_name) for p in db.session.query(models.Project).all()]
        form.inputStatus.choices = [(p.status_id, p.description) for p in db.session.query(models.Status).all()]

        if form.validate_on_submit():
            new_task = models.Task(
                description=form.inputDescription.data,
                priority_id=form.inputPriority.data,
                project_id=form.inputProject.data,
                deadline=form.inputDeadLine.data,
                status_id=1,
            )

            db.session.add(new_task)
            db.session.commit()
            return redirect('/userHome')

        return render_template('newTask.html', form=form, user=user)
    return redirect('/')


@app.route('/deleteTask/<int:task_id>', methods=['GET', 'POST'])
def deleteTask(task_id):
    _user_id = session.get('user')
    if _user_id:
        task = db.session.query(models.Task).filter_by(task_id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        return redirect('/userHome')

    return redirect('/')


@app.route('/editTask/<int:task_id>', methods=['GET', 'POST'])
def editTask(task_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = TaskForm()
        form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
        form.inputPriority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
        form.inputProject.choices = [(p.project_id, p.project_name) for p in db.session.query(models.Project).all()]
        form.inputStatus.choices = [(p.status_id, p.description) for p in db.session.query(models.Status).all()]

        if form.validate_on_submit():
            task_to_edit = db.session.query(models.Task).get(task_id)

            print('task_to_edit:', task_to_edit)

            task_to_edit.description = form.inputDescription.data
            task_to_edit.deadline = form.inputDeadLine.data
            task_to_edit.project_id = form.inputProject.data
            task_to_edit.priority_id = form.inputPriority.data
            task_to_edit.status_id = form.inputStatus.data

            db.session.commit()
            return redirect('/userHome')

        task = db.session.query(models.Task).get(task_id)
        form.inputDescription.data = task.description
        form.inputPriority.data = task.priority_id
        form.inputDeadLine.data = task.deadline
        form.inputStatus.data = task.status_id
        return render_template('newTask.html', form=form, user=user, task=task)
    return redirect('/')


@app.route('/doneTask', methods=['GET', 'POST'])
def doneTask():
    _user_id = session.get('user')
    if _user_id:
        _task_id = request.form['hiddenTaskId']
        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id = _task_id).first()
            task.isCompleted = True
            db.session.commit()

        return redirect('/userHome')
    return redirect('/')


@app.route('/projectHome', methods=['GET', 'POST'])
def project_Home():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()
        return render_template('home-project.html', user = user)
    else:
        return redirect('/signIn')


@app.route('/deleteProject/<int:project_id>', methods=['GET', 'POST'])
def deleteProject(project_id):
    _user_id = session.get('user')
    if _user_id:

        project = db.session.query(models.Project).filter_by(project_id=project_id).first()
        db.session.delete(project)
        db.session.commit()
        return redirect('/userHome')

    return redirect('/')


@app.route('/editProject/<int:project_id>', methods=['GET', 'POST'])
def editProject(project_id):
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = AddProjectForm()
        project = db.session.query(models.Project).filter_by(project_id=project_id).first()

        if form.validate_on_submit():
            project.project_name = form.inputName.data
            project.project_deadline = form.inputDeadline.data
            project.description = form.inputDescription.data
            db.session.commit()
            return redirect('/userHome')

        form.inputDescription.data = project.description
        form.inputName.data = project.project_name
        form.inputDeadline.data = project.project_deadline
        return render_template('newProject.html', form=form, user=user, project=project)

    return redirect('/')


@app.route('/newProject', methods=['GET', 'POST'])
def newProject():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        form = AddProjectForm()
        if form.validate_on_submit():
            _name = form.inputName.data
            _description = form.inputDescription.data
            _deadline = form.inputDeadline.data

            project = models.Project(description=_description, project_name=_name, project_deadline=_deadline, user=user, status_id=1)
            db.session.add(project)
            db.session.commit()
            return redirect('/userHome')

        return render_template('/newProject.html', form=form, user=user)

    # not logged in user --> redirect to normal page
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port="8080", debug=True)