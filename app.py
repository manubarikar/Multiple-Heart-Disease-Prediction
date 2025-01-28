from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
import pickle
import numpy as np

app = Flask(__name__)


model2 = pickle.load(open('heart_model2.pkl', 'rb'))
model3 = pickle.load(open('CAD1.pkl', 'rb'))
model4 = pickle.load(open('Chd_rf.pkl', 'rb'))



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username 
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('uname')
        user = User(fname=fname, lname=lname, email=email, password=password, username=username)
        db.session.add(user)
        db.session.commit()
        flash('user has been registered successfully','success')
        return redirect('/login')
    return render_template("Register1.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/index')
        else:
            flash('Invalid Credentials', 'warning')
            return redirect('/login')
    return render_template("login.html")


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact1')
def contact1():
    return render_template('contact1.html')


@app.route('/DataAnalytics1')
def DataAnalytics1():
    return render_template('DataAnalytics1.html')

@app.route('/Dataset1')
def Dataset1():
    return render_template('Dataset1.html')


@app.route('/home1')
def home1():
    return render_template('home1.html')


@app.route('/models')
def models():
    return render_template('models.html')

@app.route('/Model1')
def Model1():
    return render_template('Model1.html')

@app.route('/Prediction1')
def Prediction1():
    return render_template('Prediction1.html')

@app.route('/Prediction2')
def Prediction2():
    return render_template('Prediction2.html')

@app.route('/Prediction3')
def Prediction3():
    return render_template('Prediction3.html')

@app.route('/predict2', methods = ['GET', 'POST'])
def predict2():
    int_features = [  x for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction_1 = model2.predict(final_features)

    output = prediction_1[0]
    print (output)
    
    if output == 1:
        return render_template('Prediction1.html', prediction_text= 'You are suffering from Cardio Vascular Disease')
    else:
        return render_template('Prediction1.html', prediction_text= 'Ouch! You are not suffering from Cardio Vascular Disease')




@app.route('/predict3', methods = ['GET', 'POST'])
def predict3():
    int_features = [  x for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction_2 = model3.predict(final_features)

    output = prediction_2[0]
    print (output)
    
    if output == 0:
        return render_template('Prediction3.html', prediction_text= 'You are not suffering from Coronary Artery Disease')
    else:
        return render_template('Prediction3.html', prediction_text= 'You are suffering from Coronary Artery Disease')



@app.route('/predict4', methods = ['GET', 'POST'])
def predict4():
    int_features = [  x for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction_3 = model4.predict(final_features)

    output = prediction_3[0]
    print (output)
    
    if output == 1:
        return render_template('Prediction2.html', prediction_text='You are suffering from Congenital Heart Defect')
        #return render_template('Prediction2.html', prediction_text='Ouch! You are not having Congenital Heart Defect')
    else:
        return render_template('Prediction2.html', prediction_text='Ouch! You are not suffering from Congenital Heart Defect')
       #return render_template('Prediction2.html', prediction_text='You are having Congenital Heart Defect')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8081, debug=True)