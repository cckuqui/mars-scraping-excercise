from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    if mars is  None :
        mars = {
        'ntitle':'',
        'nbody':'',
        'feat_img':'',
        'img_det':'',
        'weather':'',
        'facts':'',
        'h':'',
        'date':''
        }

    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route('/scrape/')
def scrape():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape()
    mars.replace_one({}, mars_data, upsert=True)
    print(mars_data)
    return redirect("/")

@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

