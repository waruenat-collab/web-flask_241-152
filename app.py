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

@app.route("/add-restaurant", methods=["GET", "POST"])
def add_restaurant():
    if request.method == "POST":
        r = Restaurant(
            name=request.form["name"],
            location=request.form["location"],
            description=request.form["description"]
        )
        db.session.add(r)
        db.session.commit()
        return redirect("/restaurants")
    return render_template("add_restaurant.html")

@app.route("/restaurants/<int:id>")
def restaurant_detail(id):
    r = Restaurant.query.get_or_404(id)
    return render_template("restaurant_detail.html", restaurant=r)

@app.route("/restaurants/<int:id>/edit", methods=["GET", "POST"])
def edit_restaurant(id):
    r = Restaurant.query.get_or_404(id)
    if request.method == "POST":
        r.name = request.form["name"]
        r.location = request.form["location"]
        r.description = request.form["description"]
        db.session.commit()
        return redirect(f"/restaurants/{id}")
    return render_template("edit_restaurant.html", restaurant=r)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)