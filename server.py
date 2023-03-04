import datetime
from flask import Flask, render_template, url_for    # render - copy, url_for()

app = Flask(__name__)

@app.route('/') 
@app.route('/home')   # деккортатор 
def index():          # возвращает текст, который выводим на сайте
    return render_template('index.html')    # связка с html


@app.route('/about')    
def about():            
    return render_template('about.html')


@app.route('/test_page')    
def test():            
    return render_template('test.html')


@app.route('/report')    
def look_report():            
    return render_template('report.html')


@app.route('/user/<string:name>/<int:id>')   
def usert(name, id):     
    return "User page: "+ name + " - " + str(id)


if __name__ == "__mane__":
    app.run(debug=True)     # запуск приложения. debug = вывод ошибок 