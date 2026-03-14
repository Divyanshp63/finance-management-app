from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from database.db import db
from models.user import User
import random
from services.email_service import send_otp_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        full_name = request.form.get("full_name")
        phone = request.form.get("phone")
        
        # Validation
        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return redirect(url_for("auth.register"))
        
        if password != password_confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("auth.register"))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))
        
        # Create new user
        user = User(username=username, email=email, full_name=full_name, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@auth_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        new_username = request.form.get("username")
        new_email = request.form.get("email")
        
        if not new_username or not new_email:
            flash("Username and email are required.", "danger")
            return redirect(url_for("auth.edit_profile"))
            
        if new_username != current_user.username and User.query.filter_by(username=new_username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("auth.edit_profile"))
            
        if new_email != current_user.email and User.query.filter_by(email=new_email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.edit_profile"))
            
        current_user.username = new_username
        current_user.email = new_email
        current_user.full_name = request.form.get("full_name")
        current_user.phone = request.form.get("phone")
        
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("auth.profile"))
    
    return render_template("edit_profile.html", user=current_user)


@auth_bp.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash("Your account and all associated data have been permanently deleted.", "success")
    return redirect(url_for("auth.register"))
