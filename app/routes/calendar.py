from flask import Blueprint, render_template
from app.models import SeasonalEvent
from datetime import date

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/')
def calendar():
    events_by_month = {}
    for month in range(1, 13):
        events_by_month[month] = SeasonalEvent.query.filter_by(month=month).all()

    return render_template('calendar.html',
                         calendar_data=events_by_month,
                         current_month=date.today().month)
