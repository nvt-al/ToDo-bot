
from flask import Flask, render_template, url_for   # render - copy, url_for()
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import TaskForm
from flask import redirect




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
@app.route('/home')   # деккортатор 
def index():          # возвращает текст, который выводим на сайте
    return render_template('index.html')    # связка с html



@app.route('/about/', methods=['GET', 'POST'])
def about():
    form = TaskForm()
    if form.validate_on_submit():
        return redirect ('/home')
    return render_template('about.html', form=form)


# @app.route('/about/', methods=['GET', 'POST'])    
# def about():          # fix 
#     form = TaskForm()            
#     return render_template('about.html', form=form)



@app.route('/report')    
def look_report():            
    return render_template('report.html')



if __name__ == "__mane__":
    app.run(debug=True)     # запуск приложения. debug = вывод ошибок 