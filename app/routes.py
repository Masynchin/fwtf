from flask import url_for, render_template, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import *
from app.models import *
from app.utils import *


@app.route("/")
def works_log():
    jobs = Jobs.query.all()
    return render_template("works_log.html", jobs=jobs)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        
        user = User.get_by_email(email)
        if user is not None:
            flash("Email is already taken")
            return render_template("register.html", form=form)

        user = User(
            email=email, surname=form.surname.data, name=form.name.data,
            age=form.age.data, address=form.address.data,
            position=form.position.data, speciality=form.speciality.data,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)
        return redirect("/")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
            message="Неправильный логин или пароль", form=form)

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route("/addjob", methods=["GET", "POST"])
def addjob():
    form = JobForm()
    if form.validate_on_submit():
        team_leader = form.team_leader.data
        collaborators = map(int, form.collaborators.data.split(","))
        if not check_users_exists([team_leader, *collaborators]):
            flash("Incorrect team_leader or collaborator ID")
            return render_template("addjob.html", form=form)

        job = Jobs(
            job=form.job.data,
            team_leader=team_leader,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            category_id=form.category_id.data,
            is_finished=form.is_finished.data,
        )

        db.session.add(job)
        db.session.commit()
        return redirect("/")

    return render_template("addjob.html", form=form)


@app.route("/editjob/<int:job_id>", methods=["GET", "POST"])
def editjob(job_id):
    job = Jobs.query.get(job_id)
    form = JobForm()
    if form.validate_on_submit():
        if check_rights_and_noneless(current_user, job.team_lead.id, job):

            team_leader = form.team_leader.data
            collaborators = map(int, form.collaborators.data.split(","))
            if not check_users_exists([team_leader, *collaborators]):
                flash("Incorrect team_leader or collaborator ID")
                return render_template("addjob.html", form=form)

            job.team_leader = team_leader
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.category_id = form.category_id.data
            job.is_finished = form.is_finished.data

            db.session.commit()
            return redirect("/")

        else:
            flash("Not enough rights for that action")
            return redirect("/")

    if check_rights_and_noneless(current_user, job.team_lead.id, job):
        return render_template("addjob.html", form=form)

    else:
        flash("Not enough rights for that action")
        return redirect("/")


@app.route("/deljob/<int:job_id>")
def deljob(job_id):
    job = Jobs.query.get(job_id)
    if (
        current_user.is_authenticated and
        current_user.id in (job.team_lead.id, 1)
    ):
        db.session.delete(job)
        db.session.commit()
        flash("Succecsfully delete")
    return redirect("/")


@app.route("/departments")
def departments():
    departments = Department.query.all()
    return render_template("departments.html", departments=departments)


@app.route("/add_department", methods=["GET", "POST"])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        chief = form.chief.data
        members = map(int, form.members.data.split(","))
        if not check_users_exists([chief, *members]):
            flash("Incorrect team_leader or collaborator ID")
            return render_template("adddepartment.html", form=form)

        department = Department(title=form.title.data,
            chief=chief, members=form.members.data, email=form.email.data)
        db.session.add(department)
        db.session.commit()
        return redirect("/")

    elif not current_user.is_authenticated:
        flash("Not enough rights for that action")
        return redirect("/")

    return render_template("adddepartment.html", form=form)


@app.route("/edit_department/<int:department_id>", methods=["GET", "POST"])
def edit_department(department_id):
    department = Department.query.get(department_id)
    form = DepartmentForm()
    if form.validate_on_submit():
        if check_rights_and_noneless(current_user, department.chief, department):
            chief = form.chief.data
            members = map(int, form.members.data.split(","))
            if not check_users_exists([chief, *members]):
                flash("Incorrect team_leader or collaborator ID")
                return render_template("adddepartment.html", form=form)

            department.title = form.title.data
            department.chief = chief
            department.members = form.members.data
            department.email = form.email.data

            db.session.commit()
            return redirect("/")

        else:
            flash("Not enough rights for that action")
            return redirect("/")

    if check_rights_and_noneless(current_user, department.chief, department):
        return render_template("adddepartment.html", form=form)

    else:
        flash("Not enough rights for that action")
        return redirect("/")


@app.route("/del_department/<int:department_id>", methods=["GET", "POST"])
def del_department(department_id):
    department = Department.query.get(department_id)
    if (
        current_user.is_authenticated and
        current_user.id in (department.chief, 1)
    ):
        db.session.delete(department)
        db.session.commit()
        flash("Succecsfully delete")
    return redirect("/departments")
