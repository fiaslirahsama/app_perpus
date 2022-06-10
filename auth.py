import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskbooknew.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama']
        db = get_db()
        error = None

        if not username:
            error = "Masukkan username"
        elif not password:
            error = "Masukkan password"
        elif not nama:
            error = "Masukkan nama"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO admin (username, password, nama) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), nama),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} telah terdaftar."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        admin = db.execute(
            'SELECT * FROM admin WHERE username = ?', (username,)
        ).fetchone()

        if admin is None:
            error = 'Username salah/ tidak terdaftar, silahkan coba lagi'
        elif not check_password_hash(admin['password'], password):
            error = 'Password salah, silahkan coba lagi.'

        if error is None:
            session.clear()
            session['admin_id'] = admin['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    admin_id = session.get('admin_id')

    if admin_id is None:
        g.admin = None
    else:
        g.admin = get_db().execute(
            'SELECT * FROM admin WHERE id = ?', (admin_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view