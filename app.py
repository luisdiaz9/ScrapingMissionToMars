from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scraper

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" 
mongo = PyMongo(app)
mongo.db.DataToHTML.drop()

@app.route("/")
def home(): 
    DataToHTML = mongo.db.DataToHTML.find_one()
    return render_template("index.html", DataToHTML = DataToHTML)

#  function called scrape that will execute all of your scraping code
@app.route("/scrape")
def scrape(): 

    # execution of the entire scraping code
    DataToHTML = mongo.db.DataToHTML
    data = scraper.scrape_last()
    data = scraper.scrape_img()
    data = scraper.scrape_msg()
    data = scraper.scrape_table()
    data = scraper.scrape_imgs()
    DataToHTML.update({}, data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)