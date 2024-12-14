from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database
import os

app = Flask(__name__)
# Generar clave secreta para Termux
app.secret_key = os.urandom(24)
db = Database()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario = db.validar_usuario(username, password)
        
        if usuario:
            session['user_id'] = usuario[0]
            session['username'] = usuario[1]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = request.form.get('rol', 'Empleado')
        nombre = request.form.get('nombre', '')
        email = request.form.get('email', '')
        
        if db.registrar_usuario(username, password, rol, nombre, email):
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error: El usuario ya existe', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    registros = db.obtener_registros(session['user_id'])
    return render_template('dashboard.html', registros=registros, username=session['username'])

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if db.realizar_checkin(session['user_id']):
            flash('Check-in realizado exitosamente', 'success')
        else:
            flash('Error al realizar check-in', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('checkin.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if db.realizar_checkout(session['user_id']):
        flash('Check-out realizado exitosamente', 'success')
    else:
        flash('Error al realizar check-out', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Configuración para Termux
    app.run(debug=True, host='0.0.0.0', port=5000)

