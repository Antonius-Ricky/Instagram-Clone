from flask import render_template, redirect, url_for, flash, request, make_response,jsonify
from flask_login import login_user, login_required, logout_user, current_user

from application import app
import os
from application.models import *
from application.forms import *
from application.utils import save_image, save_profile_picture


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile',username=current_user.username))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile', username=current_user.username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', title=f'{current_user.fullname} Profile')

@app.route('/<string:username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        filename = user.profile_pic
        posts = current_user.posts
        reverse_posts = posts[::-1]
        return render_template('profile.html', title=f'{current_user.fullname} Profile', posts=reverse_posts, filename=filename, user=user)
    else:
        flash('User not found', 'error')
        return redirect(url_for('index'))
    
@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        post = Post(
            author_id = current_user.id,
            caption =form.caption.data
        )
        
        post.photo = save_image(form.post_pic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted ❤!', "success")
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id = current_user.id).order_by(Post.post_date.desc()).paginate(page=page, per_page=3)
    return render_template('index.html', title='Home', form=form, posts=posts)


@app.route('/signup',methods=('GET', 'POST'))
def signup():
    if current_user.is_authenticated: 
        return redirect(url_for('profile', username=current_user.username))
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            fullname = form.fullname.data,
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))


    return render_template('signup.html', title="SignUp", form=form)
    
@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/forgotpassword')
def forgotpassword():
    form = ForgotPasswordForm()
    return render_template('forgot_password.html', title='ForgotPassword', form=form)

@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    filename = None  # Set a default value

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.username = form.username.data
        user.fullname = form.fullname.data
        user.bio = form.bio.data

        if form.profile_pic.data:
            if form.profile_pic.validate(form):
                filename = os.path.basename(save_profile_picture(form.profile_pic.data))
                user.profile_pic = filename

        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile', username=current_user.username, filename=filename))

    form.username.data = current_user.username
    form.fullname.data = current_user.fullname
    form.bio.data = current_user.bio
    form.profile_pic.data = current_user.profile_pic

    return render_template('profile_edit.html', title=f'Edit {current_user.username} Profile', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(password=form.old_password.data).first()

        if user:
            user.password = form.new_password.data
            db.session.commit()
            flash('password reset successfully!', 'success')
            return redirect(url_for('verif'))
        else:
            flash('old password is incorrect!', 'danger')
    return render_template('reset_password.html', title=f'Change {current_user.fullname} Password', form=form)

@app.route('/verif',  methods=['GET', 'POST'])
@login_required
def verif():
    form = VerificationResetPasswordForm()

    if form.validate_on_submit():
        password = form.password.data

        user = User.query.get(current_user.id)
        if  password == user.password:
            login_user(user)
            flash('Password verified successfully!', 'success')
            return redirect(url_for('profile', username=current_user.username))
        else:
            flash('Invalid password. Please try again.', 'error')

    return render_template('verif.html', title='Verification', form=form)

@app.route('/createpost')
def createpost():
    form = CreatePostForm()
    return render_template('create_post.html', title='Create Post', form=form)

@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    form = EditPostForm()

    post = Post.query.get(post_id)
    if form.validate_on_submit():
        post.caption = form.caption.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))

    elif request.method == 'GET':
        form.caption.data = post.caption

    return render_template('edit_post.html', title='Edit Post', form=form, post=post)

@app.route('/like', methods=['GET','POST'])
@login_required
def like(post_id):
    data = request.json
    post_id = int(data['postId'])
    like = Like.query.filter_by(user_id = current_user, post_id=post_id).first()
    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return make_response(200, jsonify({"status" : True}), 200)
    
    db.session.delete(like)
    db.session.commit()
    return make_response(200, jsonify({"status" : False}), 200)
    







