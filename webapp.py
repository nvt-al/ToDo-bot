
from flask import Flask, render_template, url_for, redirect, flash
from flask import request 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import TaskForm




app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"

# db = SQLAlchemy(app)

# with app.app_context():
#     db.create_all()


# class Article(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(300), nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)

    


#     def __repr__(self):
#         return '<Article %r>' % self.id    # ссылка с id

@app.route('/') 
@app.route('/home', methods=['GET', 'POST'])   # деккортатор 
def index():
    form = TaskForm()
    if request.method == 'POST':
        if request.form.get['submit_button'] == 'Выполнено':
            return render_template('index.html', form=form) # do something
        elif request.form.get['submit_button'] == 'Отменить':
            return render_template('index.html', form=form) # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('index.html', form=form)          # возвращает текст, который выводим на сайте
        # связка с html


# Create Class Form
@app.route('/about/', methods = ['GET', 'POST'])
def about():
    form = TaskForm()
    if form.validate_on_submit():
        # flash("Заметка создана")
        return redirect('/index')

    return render_template('about.html', 
        title = 'Создать',
        form = form)



@app.route('/report')    
def look_report():            
    return render_template('report.html')



if __name__ == "__mane__":
    app.run(debug=True)     # запуск приложения. debug = вывод ошибок 