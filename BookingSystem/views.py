from flask import Blueprint, render_template, request, flash, redirect, url_for
from .userModel import Booking
from . import db
from flask_login import login_user, logout_user, current_user, login_required
from calendar import monthrange
from datetime import datetime, date

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    #return "<h1>Test</h1>"
    if current_user.is_authenticated:
            return render_template("home.html", user = current_user )
    
    else:
        return render_template("login.html")

@views.route('/Calendar')
@views.route('/Calendar/<int:year>/<int:month>/', methods=['GET','POST'])
def calendar_view(year=None, month=None):
    # 1. Default to today if no year/month in URL
    today = date.today()
    if year is None or month is None:
        year, month = today.year, today.month

    # 2. Compute how many blanks before 1st
    first_day = date(year, month, 1)
    start_weekday = (first_day.weekday() + 1) % 7  # Sunday=0
    days_in_month = monthrange(year, month)[1]

    calendar_days = [None]*start_weekday \
                    + [date(year, month, d) for d in range(1, days_in_month+1)]
    # pad end to full weeks
    while len(calendar_days) % 7:
        calendar_days.append(None)

    # 3. Compute prev / next month
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    return render_template('calendar.html',
                           calendar_days=calendar_days, year=year, month=month, prev_year=prev_year, prev_month=prev_month, next_year=next_year, next_month=next_month, user = current_user)

@views.route('/book-training', methods=['POST'])
def book_training():
    name = request.form.get('name')
    training_type = request.form.get('training_type')
    date_str = request.form.get('date')

    # Convert date string to Python date object
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        flash("Invalid date", "danger")
        return redirect(url_for('calendar_view'))

    # Map training_type to time_slot
    training_to_slot = {
        'full_day': '09:00 - 16:00',
        'morning_half': '09:00 - 12:00',
        'afternoon_half': '13:00 - 16:00'
    }
    time_slot = training_to_slot.get(training_type)

    if not time_slot:
        flash("Invalid training type selected", "danger")
        return redirect(url_for('calendar_view'))
    
    if request.method == 'POST':

        # Create new booking
        booking = Booking(
            user_id=current_user.id if current_user.is_authenticated else None,
            name=name,
            date=date,
            training_type=training_type,
            time_slot=time_slot
        )
        db.session.add(booking)
        db.session.commit()
        flash("Booking saved successfully!", "success")

    else:
        flash("Booking Failed", "Error")


    return redirect(url_for('calendar_view'))


