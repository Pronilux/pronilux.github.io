import sqlite3
import hashlib
from datetime import datetime, date

class Database:
    def __init__(self, db_name='control_horas.db'):
        # Ruta específica para Termux
        import os
        self.db_path = os.path.join(os.path.expanduser('~'), 'control_horas.db')
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            nombre TEXT,
            email TEXT
        )''')

        # Tabla de registros de tiempo
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros_tiempo (
            id INTEGER PRIMARY KEY,
            usuario_id INTEGER,
            fecha DATE,
            hora_entrada DATETIME,
            hora_salida DATETIME,
            horas_trabajadas REAL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )''')
        
        self.conn.commit()

    def hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def registrar_usuario(self, username, password, rol, nombre, email):
        try:
            cursor = self.conn.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO usuarios 
                (username, password, rol, nombre, email) 
                VALUES (?, ?, ?, ?, ?)
            ''', (username, hashed_password, rol, nombre, email))
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validar_usuario(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = self.hash_password(password)
        
        cursor.execute('''
            SELECT * FROM usuarios 
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        return cursor.fetchone()

    def realizar_checkin(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            fecha_actual = date.today()
            hora_entrada = datetime.now()
            
            cursor.execute('''
                INSERT INTO registros_tiempo 
                (usuario_id, fecha, hora_entrada) 
                VALUES (?, ?, ?)
            ''', (usuario_id, fecha_actual, hora_entrada))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error en check-in: {e}")
            return False

    def realizar_checkout(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            hora_salida = datetime.now()
            
            # Obtener el último registro sin hora de salida
            cursor.execute('''
                SELECT id, hora_entrada FROM registros_tiempo 
                WHERE usuario_id = ? AND hora_salida IS NULL 
                ORDER BY hora_entrada DESC LIMIT 1
            ''', (usuario_id,))
            
            registro = cursor.fetchone()
            
            if registro:
                registro_id, hora_entrada = registro
                # Convertir hora_entrada a datetime si es necesario
                hora_entrada = datetime.strptime(hora_entrada, '%Y-%m-%d %H:%M:%S.%f')
                
                horas_trabajadas = (hora_salida - hora_entrada).total_seconds() / 3600
                
                cursor.execute('''
                    UPDATE registros_tiempo 
                    SET hora_salida = ?, horas_trabajadas = ? 
                    WHERE id = ?
                ''', (hora_salida, horas_trabajadas, registro_id))
                
                self.conn.commit()
                return True
            return False
        except Exception as e:
            print(f"Error en check-out: {e}")
            return False

    def obtener_registros(self, usuario_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT fecha, hora_entrada, hora_salida, horas_trabajadas 
            FROM registros_tiempo 
            WHERE usuario_id = ? 
            ORDER BY fecha DESC
        ''', (usuario_id,))
        return cursor.fetchall()
