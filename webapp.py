
from flask import Flask, render_template, url_for, redirect, flash
from flask import request 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import TaskForm




app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"

# db = SQLAlchemy(app)


tasks = [{'id': '01', 'name': 'Утренняя зарядка', 'time': '06:00', 'done': True},
        {'id': '02', 'name': 'Уроки Python', 'description': '15 мин занятия', 'done': False},
        {'id': '03', 'name': 'Уроки English', 'description': '15 мин занятия', 'done': False},
        {'id': '04', 'name': 'Слова English', 'description': 'Выучить 5 новых слов', 'done': True},
        {'id': '05', 'name': 'Лекарства', 'time': '12:15', 'done': False}]
print(tasks)

@app.route('/')
def index():
    form = TaskForm()
    return render_template('index.html', tasks=tasks, form=form)




@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if request.method == 'POST':
        # id = request.form['id']
        to_time = request.form['to_time']
        to_date = request.form['to_date']
        new_task = request.form['new_task']
        description_task = request.form['description_task']
        # done = request.form['done']
        task = {'name': new_task, 'description': description_task, 'date': to_date, 'time': to_time}
        tasks.append(task)
        print(task)
        flash('Задача добавлена!')
        return redirect(url_for('index'))
    return render_template('add_task.html', title='Add Task', form=form)

# @app.route('/add_task', methods=['POST', 'GET'])
# def add_task():
#     id = request.form['id']
#     name = request.form['name']
#     description = request.form['description']
#     done = request.form['done']
#     task = {'id': id, 'done': done, 'name': name, 'description': description}
#     tasks.append(task)
#     print(tasks)
#     return redirect(url_for('index'))





@app.route('/report')    
def look_report():            
    return render_template('report.html')



if __name__ == "__mane__":
    app.run(debug=True)     # запуск приложения. debug = вывод ошибок 