
from flask import Flask, render_template, url_for   # render - copy, url_for()
from flask_sqlalchemy import SQLAlchemy
# from app import app, db
from datetime import datetime
# from ToDo-bot.forms import TaskForm



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    


    def __repr__(self):
        return '<Article %r>' % self.id    # ссылка с id




@app.route('/') 
@app.route('/home')   # деккортатор 
def index():          # возвращает текст, который выводим на сайте
    return render_template('index.html')    # связка с html


@app.route('/about')    
def about():            
    return render_template('about.html')


# @app.route('/add_task')    
# def add_task():  
#     title = 'Добавить напоминание'   
#     login_form = TaskForm()       
#     return render_template('task.html', page_title = title, form = login_form)


@app.route('/report')    
def look_report():            
    return render_template('report.html')



if __name__ == "__mane__":
    app.run(debug=True)     # запуск приложения. debug = вывод ошибок 