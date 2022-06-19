from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_moment import Moment
import traceback

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
moment = Moment(app)


# создание класса с таблицей базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, primary_key=False)
    email = db.Column(db.String, nullable=False, primary_key=False)
    text = db.Column(db.Text, nullable=False, primary_key=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/')
def index():
    return render_template('/main.html')


@app.route('/', methods=['POST'])  # получение данных при помощи POST
def cf():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        text = request.form['text']

        user = User(name=name, email=email, text=text)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')

        except:
            print('Ошибка:\n', traceback.format_exc())
            return ''
    else:
        return render_template('html/main.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)
