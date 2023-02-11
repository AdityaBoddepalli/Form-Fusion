from flask import Blueprint, render_template
import urllib.request, json

site = Blueprint('site', __name__, template_folder='app/templates')

@site.route('/')
def landing_page():
    return render_template('index.html')