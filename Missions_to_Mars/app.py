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
    
    mars = mongo.db.collection.find_one()
    if mars is  None :
        mars = {
            'ntitle':'',
            'nbody':'',
            'feat_img':'',
            'weather':'',
            'facts':'',
            'h':''}
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape/")
def scrape():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape()
    mars.replace_one({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

