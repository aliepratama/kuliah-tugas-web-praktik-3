from flask import Flask, render_template, session, request, redirect, url_for
from supabase import create_client, Client
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.route('/', methods=["GET"])
def home():
    if session.get('is_logged_in'):
        if session.get('is_admin'):
            return redirect('/admin/list')
        return render_template('dashboard_user.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/admin/list', methods=["GET"])
def admin_list():
    if session.get('is_logged_in'):
        if session.get('is_admin'):
            users = supabase.table('coba_akun').select('*').execute()
            return render_template('dashboard_admin.html', page='list', username=session['username'], users=users.data)
        return redirect('/')
    return redirect(url_for('login'))

@app.route('/admin/register', methods=["GET"])
def admin_register():
    if session.get('is_logged_in'):
        if session.get('is_admin'):
            return render_template('dashboard_admin.html', page='register', username=session['username'])
        return redirect('/')
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        response = supabase.table('coba_akun').select('*').eq('email', email).execute()
        if len(response.data) > 0:
            if check_password_hash(response.data[0]['password'], password):
                session['is_logged_in'] = True
                session['username'] = response.data[0]['username']
                session['is_admin'] = response.data[0]['access'] == 'admin'
                return render_template('login.html', status='Berhasil')
        return render_template('login.html', status='Gagal')
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        access = request.form.get("access")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            response = supabase.table('coba_akun').insert([{
                'username': username,
                'email': email,
                'password': hashed_password,
                'access': access
            }]).execute()
            if response:
                if access == 'admin':
                    return render_template('dashboard_admin.html', status='Berhasil')
                return render_template('register.html', status='Berhasil')
        return render_template('register.html', status='Gagal')
    return render_template('register.html')

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect('/')

@app.route('/delete', methods=["POST"])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        response = supabase.table('coba_akun').delete().eq('id', id).execute()
        return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)