# -*- coding: utf-8 -*-

"""
Módulo responsable de todas las interacciones con la base de datos SQLite.
Esta versión implementa programación defensiva y transacciones para máxima robustez.
"""

import sqlite3
from typing import Dict, Any, Optional

DB_PATH = "database/careerforge.db"

class DatabaseManager:
    """
    Gestiona la conexión, configuración y operaciones CRUD con la base de datos SQLite.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Establece y devuelve una conexión a la base de datos."""
        conn = sqlite3.connect(self.db_path)
        # Permite acceder a las columnas por su nombre, como un diccionario.
        conn.row_factory = sqlite3.Row
        return conn

    def setup_database(self) -> None:
        """Crea las tablas de la base de datos si no existen."""
        # El esquema permite valores NULL en la mayoría de los campos para ser flexible.
        schema = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            email TEXT,
            linkedin TEXT,
            phone TEXT,
            base_summary TEXT
        );
        CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT,
            company TEXT,
            period TEXT,
            FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experience_id INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY (experience_id) REFERENCES experiences (id) ON DELETE CASCADE
        );
        """
        try:
            with self._get_connection() as conn:
                conn.executescript(schema)
        except sqlite3.Error as e:
            print(f"Error al configurar la base de datos: {e}")
            raise

    def save_profile(self, profile_data: Dict[str, Any]) -> None:
        """
        Guarda o actualiza un perfil de usuario completo de forma segura y transaccional.
        Maneja datos incompletos sin fallar.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Iniciar una transacción para asegurar la integridad de los datos (todo o nada).
            cursor.execute("BEGIN TRANSACTION;")
            try:
                # Limpiar datos antiguos para el usuario (ID=1 para esta app de un solo usuario)
                cursor.execute("DELETE FROM user WHERE id = 1;")
                
                # --- Guardado Defensivo de Datos de Usuario ---
                # Usamos `get()` con un valor por defecto para evitar errores si las claves no existen.
                contact_info = profile_data.get('contact') or {}
                user_tuple = (
                    1, # ID de usuario hardcodeado
                    profile_data.get('full_name'),
                    contact_info.get('email'),
                    contact_info.get('linkedin'),
                    contact_info.get('phone'),
                    profile_data.get('base_summary')
                )
                cursor.execute(
                    "INSERT INTO user (id, full_name, email, linkedin, phone, base_summary) VALUES (?, ?, ?, ?, ?, ?);",
                    user_tuple
                )

                # --- Guardado Defensivo de Experiencias y Logros ---
                # Usamos `get('experiences', [])` para iterar sobre una lista vacía si la clave no existe.
                for exp in profile_data.get('experiences', []):
                    cursor.execute(
                        "INSERT INTO experiences (user_id, role, company, period) VALUES (1, ?, ?, ?);",
                        (exp.get('role'), exp.get('company'), exp.get('period'))
                    )
                    experience_id = cursor.lastrowid
                    
                    # El mismo patrón defensivo para los logros dentro de cada experiencia.
                    for ach in exp.get('achievements', []):
                        cursor.execute(
                            "INSERT INTO achievements (experience_id, description) VALUES (?, ?);",
                            (experience_id, ach.get('description'))
                        )
                
                # Si todo ha ido bien, confirma todos los cambios en la base de datos.
                conn.commit()
                print("Perfil guardado con éxito en la base de datos.")

            except sqlite3.Error as e:
                # Si ocurre cualquier error, deshace todos los cambios desde el "BEGIN TRANSACTION".
                print(f"Error durante la transacción. Se revirtieron los cambios: {e}")
                conn.rollback()
                raise

    def load_profile(self) -> Optional[Dict[str, Any]]:
        """
        Carga el perfil completo del usuario y lo reconstruye en un diccionario de Python limpio.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM user WHERE id = 1;")
                user_row = cursor.fetchone()
                if not user_row:
                    return None  # No hay perfil guardado.
                
                # Reconstruir el perfil base
                profile = {
                    "full_name": user_row['full_name'],
                    "base_summary": user_row['base_summary'],
                    "contact": {
                        "email": user_row['email'],
                        "linkedin": user_row['linkedin'],
                        "phone": user_row['phone']
                    },
                    "experiences": [] # Asegurarse de que la clave siempre exista
                }
                
                # Obtener experiencias y sus logros anidados
                cursor.execute("SELECT * FROM experiences WHERE user_id = 1 ORDER BY id;")
                for exp_row in cursor.fetchall():
                    experience = dict(exp_row)
                    experience['achievements'] = [] # Asegurarse de que la clave siempre exista
                    
                    cursor.execute("SELECT * FROM achievements WHERE experience_id = ? ORDER BY id;", (experience['id'],))
                    ach_rows = cursor.fetchall()
                    if ach_rows:
                        experience['achievements'] = [dict(ach_row) for ach_row in ach_rows]
                    
                    profile['experiences'].append(experience)
                    
                return profile
        except sqlite3.Error as e:
            print(f"Error al cargar el perfil desde la base de datos: {e}")
            return None

# Instancia global para ser usada por la aplicación
db_manager = DatabaseManager()

# Crear la estructura de la DB al iniciar el módulo, si es necesario
db_manager.setup_database()
