from flask import Flask,render_template,request,redirect
import url_utils as shortener
from flask_sqlalchemy import SQLAlchemy
from time import gmtime, strftime
from datetime import datetime
import pyperclip

def addToDatabase(database,url_objet):
    try:
        database.session.add(url_objet)
        database.session.commit()
    except: 
        print("Cannot add to database")
def checkExistenceInDatabase(database,site):
    a = database.query.filter_by(shortURL = site).first()
    if a is None:
        return False
    else:
        return True
# Create the application.
app = Flask(__name__)
# Create the database model
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URLS.db'
db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False
class URLS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique =True,nullable=True)
    shortURL = db.Column(db.String(30), unique=True, nullable=False)
    originalURL = db.Column(db.String(1000), unique=False, nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return f"User('{self.id}', '{self.email}', Short URL: '{self.shortURL}', Long URL: '{self.originalURL}',{self.created_at})"
@app.route('/',methods=["GET","POST"])
def index():
    short_url = ''
    original_url=''
    if request.method == "POST":
        if request.form.get("shortenerButton"):
            original_url = request.form['original_url']
            #Check if new URL is already existed in database ?
            while True:
                short_url = shortener.shorten_url(original_url)
                if (checkExistenceInDatabase(URLS,short_url) == False):
                    new_url = URLS(shortURL=short_url,originalURL=original_url)
                    break
            addToDatabase(db,new_url)
            print("Short url => " + str(short_url))
        elif request.form.get("copyButton"):
            original_url = str(request.form['original_url'])
            short_url=str(request.form["shortened_URL"])
            pyperclip.copy(str(request.form["shortened_URL"]))
    
    return render_template('homepage.html',short_url = short_url,original_url=original_url)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/prevURLs',methods=["GET","POST"])
def prev():
    if request.method == "POST":
        deletedURL = request.form.get('shortURL')
        print('\n\n\n\n')
        print((deletedURL))
        print('\n\n\n\n')
        deletedURL = db.session.query(URLS).filter_by(shortURL=deletedURL).first()
        print('\n\n\n\n')
        print((deletedURL))
        print('\n\n\n\n')
        db.session.delete(deletedURL)
        db.session.commit()
    past_urls = URLS.query.order_by(URLS.created_at)
    
    return render_template('prev.html',past_urls = past_urls)
@app.route('/<id>')
def gotosite(id):
    print("Tryig to reach the site")
    try:
        site = URLS.query.filter_by(shortURL=shortener.get_url_by_ID(id)).first()
        last_site = shortener.checkForHTTP(site.originalURL)
        return redirect(last_site)   
    except:
        return("Sorry This page is not available!")

if __name__ == '__main__':
    app.debug=True
    app.run()