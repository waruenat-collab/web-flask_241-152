from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'food.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/restaurants")
def restaurants():
    data = Restaurant.query.all()
    return render_template("restaurants.html", restaurants=data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)