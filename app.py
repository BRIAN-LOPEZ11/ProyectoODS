from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'KEYKEYKEY1122' 

db = mysql.connector.connect(
    host="localhost",
    user="ADMIN1",
    password="BRIAN1107",
    database="databasedb"
)

@app.route('/')
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    correo = request.form['correo']
    password = request.form['password'].encode('utf-8')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE Correo = %s", (correo,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.checkpw(password, user['Password'].encode('utf-8')):
        session['user_id'] = user['ID']
        session['user_name'] = user['Nombre']
        return redirect(url_for('index'))
    else:
        return "Correo o contraseña incorrectos", 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password'].encode('utf-8')
        nombre = request.form['nombre']
        apellido = request.form['apellido']

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (Correo, Password, Nombre, Apellido) VALUES (%s, %s, %s, %s)",
            (correo, hashed.decode('utf-8'), nombre, apellido)
        )
        db.commit()
        cursor.close()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')
    
@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
