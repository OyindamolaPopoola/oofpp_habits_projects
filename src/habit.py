from datetime import datetime
from database.db_manager import get_connection

class Habit:
    def __init__(self, name: str, periodicity: str, created_at: str = None, id: int = None):
        self.id = id
        self.name = name
        self.periodicity = periodicity.lower()
        self.created_at = created_at if created_at else datetime.utcnow().isoformat()

    def save(self) -> bool:
        """Saves the habit definition to the database. Returns False if duplicate."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?);",
                (self.name, self.periodicity, self.created_at)
            )
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def complete_task(habit_id: int):
        """Logs a timestamp event recording that a habit was completed."""
        conn = get_connection()
        cursor = conn.cursor()
        now_str = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO records (habit_id, check_in_time) VALUES (?, ?);",
            (habit_id, now_str)
        )
        conn.commit()
        conn.close()