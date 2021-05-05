from flask import Flask,render_template,redirect,request,session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import random
import pathlib

app = Flask(__name__)
app.secret_key = 'luciferdevil'
app.config['UPLOAD'] = r'E:\Websites\pomato\static\images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/mobile'
db = SQLAlchemy(app)

class Product(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    img = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120),nullable=False)
    slug = db.Column(db.String(120), nullable=False)
    details = db.Column(db.String(120), nullable=False)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    msg = db.Column(db.String(120), nullable=False)

class Detail(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(120), nullable=False)

user = Detail.query.filter_by().first()

@app.route('/')
def home():
    mobiles = Product.query.filter_by().all()
    return render_template('index.html',mobiles=mobiles)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/special')
def special():
    return render_template('special.html')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        d = request.form.get('s')
        q = Product.query.filter_by(name=d).all()
        return render_template('search.html', q=q)
    return render_template('search.html')

@app.route('/shop/<string:slug>')
def shop(slug):
    data = Product.query.filter_by(slug=slug).first()
    return render_template('showmobile.html',data=data)

@app.route('/admin/editproduct/<string:sno>', methods=['GET','POST'])
def edit(sno):
    if ('user' in session and session['user'] == user.username):
        if request.method == 'POST':
            name = request.form.get('name')
            price = request.form.get('price')
            slug = request.form.get('slug')
            d = request.form.get('details')
            data = Product.query.filter_by(sno=sno).first()
            data.name = name
            data.price = price
            data.slug == slug
            data.details = d
            db.session.commit()
            return redirect(f'/shop/{slug}')
        t = Product.query.filter_by(sno=sno).first()
        return render_template('editmobile.html',t=t,sno=sno)
    return redirect('/admin/login')
        


@app.route('/brand')
def brand():
    data = Product.query.filter_by().all()
    return render_template('brand.html',data=data)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        msg = request.form.get('msg')
        entry = Contact(name=name,email=email,phone=phone_number,msg=msg)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')


@app.route('/admin/login',methods=['GET','POST'])
def adminlogin():
    if ('user' in session and session['user'] == user.username):
        return redirect('/admin')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pass')
        if username == user.username and password == user.password:
            session['user'] = username
            return redirect('/admin')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if ('user' in session and session['user'] == user.username):
        return render_template('admindash.html')
    return redirect('/admin/login')

@app.route('/admin/mobiles')
def mobile():
    if ('user' in session and session['user'] == user.username):
        data = Product.query.filter_by().all()
        return render_template('mobile.html',data=data)
    return redirect('/admin/login')
@app.route('/admin/addmobile', methods=['GET','POST'])
def addmobile():
    if ('user' in session and session['user'] == user.username):
        if request.method == 'POST':
            mobile_name = request.form.get('name')
            mobile_price = request.form.get('price')
            mobile_slug = request.form.get('slug')
            mobile_details = request.form.get('details')
            mobile_img = request.files['file']
            filename = str(random.randint(0,99999999)) + pathlib.Path(mobile_img.filename).suffix
            mobile_img.save(os.path.join(app.config['UPLOAD'], secure_filename(filename)))
            add = Product(name=mobile_name,price=mobile_price,img=filename, slug=mobile_slug, details=mobile_details)
            db.session.add(add)
            db.session.commit()
            return 'Mobile Add Successfully'
        return render_template('addmobile.html')
    return redirect('/admin/login')

@app.route('/admin/contact')
def contactadmin():
    if ('user' in session and session['user'] == user.username):
        data = Contact.query.filter_by().all()
        return render_template('contactadmin.html',data=data)
    return redirect('/admin/login')

@app.route('/admin/deleteproduct/<string:sno>')
def deleteproduct(sno):
    if ('user' in session and session['user'] == user.username):
        post = Product.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/admin/mobiles')
    return redirect('/admin/login')

@app.route('/logout')
def logout():
    if ('user' in session and session['user'] == user.username):
        session.pop('user')
        return redirect('/admin/login')
    return('/admin/login')

app.run(debug=True)