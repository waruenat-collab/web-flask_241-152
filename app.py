from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template
from models import db
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'food.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Restaurant

@app.route('/restaurants')
def restaurants():
    data = Restaurant.query.all()
    return render_template('restaurants.html', restaurants=data)

from flask import request, redirect, url_for
from models import Restaurant

@app.route('/add-restaurant', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']

        restaurant = Restaurant(
            name=name,
            location=location,
            description=description
        )

        db.session.add(restaurant)
        db.session.commit()

        return redirect(url_for('restaurants'))

    return render_template('add_restaurant.html')