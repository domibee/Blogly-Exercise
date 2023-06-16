"""Blogly application."""

from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.app_context().push()
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('index.html',users=users)

@app.route('/users/new')
def new_user_form():
    """Show an add form for user"""

    return render_template('form.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Form for user"""
    print ('Hello!')
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/<int:user_id>')
def user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/edit/<int:user_id>', methods=['GET','POST'])
def edit_user(user_id):

    user = User.query.get_or_404(user_id) 
    # checks if first name field exists in the request form dictionary and also checks if the value is not empty.
    # if both conditions are true the area is updated
    if request.method == 'POST':
        if 'first_name' in request.form and request.form['first_name']:
            user.first_name = request.form['first_name']
        if 'last_name' in request.form and request.form['last_name']:
            user.last_name = request.form['last_name']
        if 'image_url' in request.form and request.form['image_url']:
            user.image_url = request.form['image_url']
        db.session.commit()
        return redirect(f'/{user.id}')

    return render_template('user_edit.html',user=user)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
    
    return redirect('/')





