from flask import Blueprint, jsonify, session, request
from app.models import User, db, DirectMessage
from app.forms import LoginForm
from app.forms import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_, and_
