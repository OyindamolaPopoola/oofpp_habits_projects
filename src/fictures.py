from datetime import datetime, timedelta
from database.db_manager import get_connection

def inject_test_fixtures():
    """Pre-populates the database with 5 habits and 4 weeks of historical check-in records."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM habits;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # 5 Predefined habits
    predefined_habits = [
        ("Read data analytics articles", "daily"),
        ("Drink 3 liters of water", "daily"),
        ("Meditate for 10 minutes", "daily"),
        ("Gym workout", "weekly"),
        ("Update business ledger", "weekly")
    ]

    base_time = datetime.utcnow() - timedelta(days=29)

    for name, periodicity in predefined_habits:
        cursor.execute(
            "INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?);",
            (name, periodicity, base_time.isoformat())
        )
        habit_id = cursor.lastrowid

        # Simulating 4 weeks of historical records
        if periodicity == "daily":
            for day in range(28):
                if day == 12 and name == "Meditate for 10 minutes":
                    continue 
                check_in = base_time + timedelta(days=day, hours=9)
                cursor.execute(
                    "INSERT INTO records (habit_id, check_in_time) VALUES (?, ?);",
                    (habit_id, check_in.isoformat())
                )
        elif periodicity == "weekly":
            for week in range(4):
                check_in = base_time + timedelta(weeks=week, days=2, hours=17)
                cursor.execute(
                    "INSERT INTO records (habit_id, check_in_time) VALUES (?, ?);",
                    (habit_id, check_in.isoformat())
                )

    conn.commit()
    conn.close()
    print("✨ Test history successfully initialized!")