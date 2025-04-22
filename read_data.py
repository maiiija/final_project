from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os.path

db = SQLAlchemy()
app = Flask(__name__)
application = app 
db_name = 'phones.db'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

class Phone(db.Model):
    __tablename__ = 'phones'
    make = db.Column(db.String)
    model = db.Column(db.String)
    year = db.Column(db.String)
    shape = db.Column(db.String)
    camera = db.Column(db.String)
    videocamera = db.Column(db.String)
    internet = db.Column(db.String)
    music = db.Column(db.String)
    games = db.Column(db.String)
    keyboard = db.Column(db.String)
    image = db.Column(db.String, primary_key=True)


@app.route('/')
def index():
    images = [image[0] for image in db.session.execute(
        db.select(Phone).with_only_columns(Phone.image).distinct()
    ).all()]
    return render_template('index.html', images=images)

@app.route('/inventory/<image>')
def inventory(image):
    try:
        phones = db.session.execute(db.select(Phone)
            .filter_by(image=image)
            .order_by(Phone.image)).scalars()
        return render_template('phone.html', phones=phones, image=image)
    except Exception as e:
        
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/references')
def references():
    return render_template('references.html')


if __name__ == '__main__':

    app.run(debug=True)