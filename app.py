from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

# --------------------
# App Configuration
# --------------------
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'food.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------
# Database Model
# --------------------
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Restaurant {self.name}>'

# --------------------
# Routes
# --------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---- Restaurants ----

@app.route("/restaurants")
def restaurants():
    data = Restaurant.query.all()
    return render_template("restaurants.html", restaurants=data)

@app.route("/restaurants/<int:id>")
def restaurant_detail(id):
    restaurant = Restaurant.query.get_or_404(id)
    return render_template(
        "restaurant_detail.html",
        restaurant=restaurant
    )

@app.route("/add-restaurant", methods=["GET", "POST"])
def add_restaurant():
    if request.method == "POST":
        new_restaurant = Restaurant(
            name=request.form["name"],
            location=request.form["location"],
            description=request.form["description"]
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect("/restaurants")

    return render_template("add_restaurant.html")

@app.route("/restaurants/<int:id>/edit", methods=["GET", "POST"])
def edit_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)

    if request.method == "POST":
        restaurant.name = request.form["name"]
        restaurant.location = request.form["location"]
        restaurant.description = request.form["description"]
        db.session.commit()
        return redirect(f"/restaurants/{id}")

    return render_template(
        "edit_restaurant.html",
        restaurant=restaurant
    )

@app.route("/restaurants/<int:id>/delete")
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return redirect("/restaurants")

@app.route("/edit-restaurant/<int:id>", methods=["GET", "POST"])
def edit_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)

    if request.method == "POST":
        restaurant.name = request.form["name"]
        restaurant.location = request.form["location"]
        restaurant.description = request.form["description"]

        db.session.commit()
        return redirect("/restaurants")

    return render_template("edit_restaurant.html", restaurant=restaurant)

@app.route("/delete-restaurant/<int:id>")
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return redirect("/restaurants")

# --------------------
# Run App
# --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)