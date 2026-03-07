"""
Standalone dashboard app: same DB as main app, own auth (DashboardAdmin).
Run: FLASK_APP=app flask run --port 8051
Set DATABASE_URL or SQLALCHEMY_DATABASE_URI and DASHBOARD_SECRET_KEY.
Create first admin: python -c "from app import app, db, bcrypt; from models import DashboardAdmin; app.app_context().push(); db.create_all(); a=DashboardAdmin(email='admin@example.com', password_hash=bcrypt.generate_password_hash('yourpassword').decode()); db.session.add(a); db.session.commit(); print('Done')"
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from sqlalchemy import or_, func

app = Flask(__name__)
app.config.from_object('config')

from models import db, bcrypt, DashboardAdmin, User, Voucher, UsageCreditEntry, PendingOrder, ReferralCreditGrant

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()  # creates dashboard_admin if missing; does not overwrite existing tables


def require_auth(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('dashboard_admin_id'):
            flash('Please log in.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner


@app.route('/')
def index():
    if not session.get('dashboard_admin_id'):
        return redirect(url_for('login'))
    return redirect(url_for('dashboard_home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        if not email or not password:
            flash('Email and password required.', 'error')
            return render_template('login.html')
        admin = DashboardAdmin.query.filter_by(email=email).first()
        if admin and bcrypt.check_password_hash(admin.password_hash, password):
            session['dashboard_admin_id'] = admin.id
            session['dashboard_admin_email'] = admin.email
            return redirect(url_for('dashboard_home'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('dashboard_admin_id', None)
    session.pop('dashboard_admin_email', None)
    flash('Logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@require_auth
def dashboard_home():
    total_users = User.query.count()
    pro_users = User.query.filter(User.plan.in_(['starter', 'pro', 'master', 'monthly', 'annual'])).count()
    total_referrals = ReferralCreditGrant.query.count()
    voucher_available = Voucher.query.filter_by(status='AVAILABLE').count()
    voucher_used = Voucher.query.filter_by(status='USED').count()
    return render_template('dashboard_home.html',
        total_users=total_users, pro_users=pro_users,
        total_referrals=total_referrals, voucher_available=voucher_available, voucher_used=voucher_used)


@app.route('/dashboard/subscribers')
@require_auth
def subscribers():
    q = User.query
    search = (request.args.get('q') or '').strip()
    if search:
        q = q.filter(or_(User.email.ilike(f'%{search}%'), func.coalesce(User.phone, '').ilike(f'%{search}%')))
    plan_filter = request.args.get('plan', '').strip()
    if plan_filter:
        q = q.filter(User.plan == plan_filter)
    users = q.order_by(User.created_at.desc()).limit(500).all()
    return render_template('subscribers.html', users=users, search=search, plan_filter=plan_filter)


@app.route('/dashboard/vouchers')
@require_auth
def vouchers_list():
    vouchers = Voucher.query.order_by(Voucher.created_at.desc()).limit(200).all()
    return render_template('vouchers.html', vouchers=vouchers)


@app.route('/dashboard/vouchers/create', methods=['GET', 'POST'])
@require_auth
def voucher_create():
    if request.method == 'POST':
        code = (request.form.get('code') or '').strip().upper()
        discount_percent = request.form.get('discount_percent', type=int) or 0
        valid_from_s = request.form.get('valid_from') or '2000-01-01'
        valid_until_s = request.form.get('valid_until') or '2099-12-31'
        if not code:
            flash('Code is required.', 'error')
            return redirect(url_for('voucher_create'))
        if Voucher.query.filter_by(code=code).first():
            flash('Code already exists.', 'error')
            return redirect(url_for('voucher_create'))
        if not (1 <= discount_percent <= 100):
            flash('Discount must be 1-100.', 'error')
            return redirect(url_for('voucher_create'))
        try:
            from datetime import datetime
            valid_from = datetime.strptime(valid_from_s, '%Y-%m-%d')
            valid_until = datetime.strptime(valid_until_s, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format (YYYY-MM-DD).', 'error')
            return redirect(url_for('voucher_create'))
        if valid_until < valid_from:
            flash('End date must be after start date.', 'error')
            return redirect(url_for('voucher_create'))
        v = Voucher(code=code, status='AVAILABLE', discount_percent=discount_percent,
                    valid_from=valid_from, valid_until=valid_until)
        db.session.add(v)
        db.session.commit()
        flash(f'Voucher {code} created.', 'success')
        return redirect(url_for('vouchers_list'))
    return render_template('voucher_create.html')


@app.route('/dashboard/credit/grant', methods=['GET', 'POST'])
@require_auth
def grant_credit():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        credits = request.form.get('credits', type=int) or 0
        if not email or credits <= 0:
            flash('Valid email and positive credits required.', 'error')
            return redirect(url_for('grant_credit'))
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('grant_credit'))
        admin_id = session.get('dashboard_admin_id')
        user.credits_balance = (user.credits_balance or 0) + credits
        db.session.add(UsageCreditEntry(
            user_id=user.id, type='admin_grant', amount=credits,
            reference_type='admin_grant', reference_id=str(admin_id)
        ))
        db.session.commit()
        flash(f'Added {credits} credits to {email}.', 'success')
        return redirect(url_for('dashboard_home'))
    return render_template('grant_credit.html')


@app.route('/dashboard/orders')
@require_auth
def orders_list():
    orders = PendingOrder.query.order_by(PendingOrder.created_at.desc()).limit(200).all()
    return render_template('orders.html', orders=orders)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8051)), debug=os.environ.get('FLASK_DEBUG', '0') == '1')
