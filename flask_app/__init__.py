from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "middle-out, why didn't I think of that?"
bcrypt = Bcrypt(app)
