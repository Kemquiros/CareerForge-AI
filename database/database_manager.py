import sqlite3
from typing import Dict, Any, Optional

DB_PATH = "database/careerforge.db"

class DatabaseManager:
    """Clase para gestionar todas las interacciones con la base de datos SQLite."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def setup_database(self) -> None:
        """Crea las tablas de la base de datos si no existen."""
        schema = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT,
            linkedin TEXT,
            phone TEXT,
            base_summary TEXT
        );
        CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            company TEXT,
            period TEXT,
            FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experience_id INTEGER NOT NULL,
            description TEXT NOT NULL,
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
        """Guarda o actualiza un perfil de usuario completo en la base de datos."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")
            try:
                cursor.execute("DELETE FROM user WHERE id = 1;")
                
                user_tuple = (
                    1,
                    profile_data.get('full_name'),
                    profile_data.get('contact', {}).get('email'),
                    profile_data.get('contact', {}).get('linkedin'),
                    profile_data.get('contact', {}).get('phone'),
                    profile_data.get('base_summary')
                )
                cursor.execute(
                    "INSERT INTO user (id, full_name, email, linkedin, phone, base_summary) VALUES (?, ?, ?, ?, ?, ?);",
                    user_tuple
                )

                for exp in profile_data.get('experiences', []):
                    cursor.execute(
                        "INSERT INTO experiences (user_id, role, company, period) VALUES (1, ?, ?, ?);",
                        (exp.get('role'), exp.get('company'), exp.get('period'))
                    )
                    experience_id = cursor.lastrowid
                    for ach in exp.get('achievements', []):
                        cursor.execute(
                            "INSERT INTO achievements (experience_id, description) VALUES (?, ?);",
                            (experience_id, ach.get('description'))
                        )
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                print(f"Error durante la transacción. Se revirtieron los cambios: {e}")
                raise

    def load_profile(self) -> Optional[Dict[str, Any]]:
        """Carga el perfil completo del usuario desde la base de datos."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user WHERE id = 1;")
                user_row = cursor.fetchone()
                if not user_row:
                    return None
                
                profile = dict(user_row)
                profile['contact'] = {
                    "email": user_row['email'], "linkedin": user_row['linkedin'], "phone": user_row['phone']
                }
                profile['experiences'] = []
                
                cursor.execute("SELECT * FROM experiences WHERE user_id = 1;")
                for exp_row in cursor.fetchall():
                    experience = dict(exp_row)
                    experience['achievements'] = []
                    cursor.execute("SELECT * FROM achievements WHERE experience_id = ?;", (experience['id'],))
                    for ach_row in cursor.fetchall():
                        experience['achievements'].append(dict(ach_row))
                    profile['experiences'].append(experience)
                return profile
        except sqlite3.Error as e:
            print(f"Error al cargar el perfil: {e}")
            return None

db_manager = DatabaseManager()
db_manager.setup_database()
