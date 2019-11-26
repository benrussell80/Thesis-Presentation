from flask import Blueprint, render_template
from glob import glob
import os


slides = Blueprint('slides', __name__)

@slides.route('/slide/<int:number>')
def slide_number(number):
    number = max(number, 0)
    return render_template(f'slide{number}.html', slide_number=number, number_of_slides=37)