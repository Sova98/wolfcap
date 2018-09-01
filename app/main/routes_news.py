from app.main import bp
from flask import render_template
from app import login_manager
from app.models.user import User
from flask_login import login_required

@bp.route('/news', methods=['POST', 'GET'])
@login_required
def news():
    return render_template('news.html')
