"""Blogly application."""

from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.app_context().push()
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('/index.html',users=users)

@app.route('/users/new')
def new_user_form():
    """Show an add form for user"""

    return render_template('/users/form.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Form for user"""
    print ('Hello!')
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url" ]

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/<int:user_id>')
def user_info(user_id):
    """Show user"""
    user = User.query.get_or_404(user_id)

    return render_template('/users/profile.html', user=user)

@app.route('/edit/<int:user_id>', methods=['GET','POST'])
def edit_user(user_id):
    """Edit User"""
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

    return render_template('/users/user_edit.html',user=user)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
    
    return redirect('/')

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get_or_404(user_id) 
    """Show an post form for user"""

    return render_template('/posts/new_post.html', user= user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """Form for creating a post"""

    user = User.query.get_or_404(user_id) 
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title = title, content = content, user_id = user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user.id}')

@app.route('/users/<int:userId>/posts/<int:postId>')
def show_post(userId, postId):
    """Shows a post"""
    user = User.query.get_or_404(userId)
    post = Post.query.get_or_404(postId)
    print("*********")
    print(post)
    return render_template('/posts/post_detail_page.html', post = post, user=user)

@app.route('/posts/<int:id>/edit')
def show_edit_post(id):
    """Page to edit a post"""
    
    post = Post.query.get_or_404(id)
    
    return render_template('/posts/edit_post.html', post = post)

@app.route('/posts/<int:id>/edit', methods=['POST'])
def edit_post(id):
    """Page to edit a post"""
    
    post = Post.query.get_or_404(id)
    
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/{post.user_id}')

@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    """Delete post"""

    post = Post.query.get_or_404(id)

    if post:
        db.session.delete(post)
        db.session.commit()

    return redirect(f'/{post.user_id}') 


