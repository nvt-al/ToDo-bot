from flask import Flask, render_template, url_for, redirect, flash, request
from webapp.models import TaskTemplates, ToDoLists, Tasks, db
from webapp.forms import TaskForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from webapp.user.models import User
# from webapp.user.views import blueprint as user_blueprint



def create_app():
    
    app = Flask(__name__, template_folder='templates')
    

    app.config.from_pyfile("config.py")
    app.config['SECRET_KEY'] = 'any secret string'
    
    db.init_app(app)
    migrate = Migrate(app, db)


    @app.route("/")
    def index():
        form = TaskForm()
        tasks = TaskTemplates.query.all()
        return render_template("index.html", tasks=tasks, form=form)
    



    @app.route("/add_task", methods=["GET", "POST"])
    def add_task():
        form = TaskForm()
        print(form.validate_on_submit())
        if request.method == 'POST':
            print(form.errors)
        if form.validate_on_submit():
            name = request.form.get("name_task")
            description = request.form.get("description")
            new_task = TaskTemplates(name=name, description=description, owner=1, is_active=False)
            db.session.add(new_task)
            db.session.commit()
            flash('Задача добавлена!')    # нужно разобраться с html
            return redirect("index.html")  
        return render_template('add_task.html', form=form)




    # update task
    @app.route("/update_task/<int:task_id>", methods=["GET", "POST"])
    def update(task_id):
        task = Tasks.query.filter_by(id=task_id).first()
        if request.method == "POST":
            task.is_active = not task.is_active
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("update_task.html", task=task)


    # delete task
    @app.route("/delete_task/<int:task_id>", methods=["POST"])
    def delete_task(task_id):
        task = Tasks.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        flash("Задача удалена!")
        return redirect(url_for("index"))


    @app.route("/report")
    def look_report():
        tasks = Tasks.query.all()
        return render_template("report.html", tasks=tasks)




    if __name__ == "__main__":
        app.run(debug=True)




    return app

   

    # app.register_blueprint(user_blueprint)

    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = "login"

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(user_id)

    return app
