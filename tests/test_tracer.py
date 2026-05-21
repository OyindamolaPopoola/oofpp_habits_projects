import unittest
from datetime import datetime, timedelta
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.habit import Habit
import src.analytics as analytics
from database.db_manager import initialize_database, get_connection

class TestHabitTrackerCore(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        import database.db_manager
        database.db_manager.DB_NAME = "test_habit_tracker.db"
        initialize_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_habit_tracker.db"):
            try:
                os.remove("test_habit_tracker.db")
            except PermissionError:
                pass

    def setUp(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records;")
        cursor.execute("DELETE FROM habits;")
        conn.commit()
        conn.close()

    def test_habit_creation_and_saving(self):
        habit = Habit("Read Analytics Articles", "daily")
        success = habit.save()
        self.assertTrue(success)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, periodicity FROM habits WHERE id = ?;", (habit.id,))
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Read Analytics Articles")
        self.assertEqual(row[1], "daily")

    def test_daily_streak_calculation(self):
        base_date = datetime.now()
        dates = [
            (base_date - timedelta(days=3)).isoformat(),
            (base_date - timedelta(days=2)).isoformat(),
            (base_date - timedelta(days=1)).isoformat(),
            base_date.isoformat()
        ]
        
        streak = analytics.calculate_streak(dates, "daily")
        self.assertEqual(streak, 4)

    def test_broken_streak_calculation(self):
        """Verifies that a gap in habit completion correctly breaks and resets a tracking streak."""
        base_date = datetime.now()
        # Adjusted dates to create a clear, unambiguous break in a daily routine
        dates = [
            (base_date - timedelta(days=3)).isoformat(),
            base_date.isoformat()
        ]
        
        streak = analytics.calculate_streak(dates, "daily")
        # The old streak is broken; only the most recent day counts
        self.assertEqual(streak, 1)

    def test_periodicity_filtering(self):
        mock_habits = [
            {"id": 1, "name": "Water", "periodicity": "daily"},
            {"id": 2, "name": "Gym", "periodicity": "weekly"},
            {"id": 3, "name": "Meditate", "periodicity": "daily"}
        ]
        
        daily_habits = analytics.filter_by_periodicity(mock_habits, "daily")
        weekly_habits = analytics.filter_by_periodicity(mock_habits, "weekly")
        
        self.assertEqual(len(daily_habits), 2)
        self.assertEqual(len(weekly_habits), 1)

if __name__ == '__main__':
    unittest.main()