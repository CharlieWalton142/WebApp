from flask import Blueprint, render_template, request, flash, redirect, url_for
from .userModel import Booking
from . import db
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import extract
from calendar import monthrange
from datetime import datetime, date

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    #return "<h1>Test</h1>"
    if current_user.is_authenticated:
            return render_template("home.html", user = current_user )
    

@views.route('/Calendar')
@views.route('/Calendar/<int:year>/<int:month>/', methods=['GET', 'POST'])
def calendar_view(year=None, month=None):
    today = date.today()
    if year is None or month is None:
        year, month = today.year, today.month

    # Calendar generation
    first_day = date(year, month, 1)
    start_weekday = (first_day.weekday() + 1) % 7
    days_in_month = monthrange(year, month)[1]

    calendar_days = [None] * start_weekday + [date(year, month, d) for d in range(1, days_in_month + 1)]
    while len(calendar_days) % 7:
        calendar_days.append(None)

    # Fetch bookings for the month
    bookings = Booking.query.filter(
        db.extract('year', Booking.date) == year,
        db.extract('month', Booking.date) == month
    ).all()

    # Map bookings to days
    booked_by_day = {}
    for booking in bookings:
        booked_by_day.setdefault(booking.date.day, []).append({
            "user_id": booking.user_id,
            "training_type": booking.training_type,
            "time_slot": booking.time_slot,
        })

    # Previous / next month logic
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    return render_template(
        'calendar.html',
        calendar_days=calendar_days,
        year=year,
        month=month,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        booked_by_day=booked_by_day,
        user=current_user
    )

@views.route('/book-training', methods=['POST'])
def book_training():
    name = request.form.get('name')
    training_type = request.form.get('training_type')
    date_str = request.form.get('date')

    # Convert date string to Python date object
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        flash("Invalid date", category = 'error')
        return redirect(url_for('views.calendar_view'))

    # Map training_type to time_slot
    training_to_slot = {
        'full_day': '09:00 - 16:00',
        'morning_half': '09:00 - 12:00',
        'afternoon_half': '13:00 - 16:00'
    }
    time_slot = training_to_slot.get(training_type)

    if not time_slot:
        flash("Invalid training type selected", category = 'error')
        return redirect(url_for('views.calendar_view'))
    
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


    return redirect(url_for('views.calendar_view'))


