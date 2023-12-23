from flask import Blueprint, render_template, redirect
import time
from logger.log import time_logger

home_bp = Blueprint("home", __name__, template_folder= "templates")

@home_bp.route("/")
def home():
    start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time
    time_logger.info(f'Route: /, Time: {elapsed_time}')
    return render_template('home.html')