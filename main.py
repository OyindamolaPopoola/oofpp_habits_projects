import sys
from database.db_manager import initialize_database
from src.fixtures import inject_test_fixtures
from src.habit import Habit
import src.analytics as analytics
from database.db_manager import get_connection

def run_menu():
    initialize_database()
    inject_test_fixtures()

    while True:
        print("\n=== 📊 DIVINUS HABIT TRACKER SYSTEM ===")
        print("1. View All Currently Tracked Habits")
        print("2. View Habits by Periodicity (Daily/Weekly)")
        print("3. Create a New Custom Habit")
        print("4. Mark a Habit as Completed (Check-off)")
        print("5. View Longest Running Streak Across All Habits")
        print("6. View Longest Streak for a Specific Habit")
        print("7. Exit Application")
        
        choice = input("\nEnter your selection (1-7): ").strip()

        conn = get_connection()
        cursor = conn.cursor()

        if choice == "1":
            cursor.execute("SELECT * FROM habits;")
            habits = analytics.get_all_habits(cursor.fetchall())
            print("\n--- Tracked Habits ---")
            for h in habits:
                print(f"[{h['id']}] {h['name']} ({h['periodicity']})")
                
        elif choice == "2":
            period = input("Enter periodicity to filter (daily/weekly): ").strip().lower()
            cursor.execute("SELECT * FROM habits;")
            habits = analytics.get_all_habits(cursor.fetchall())
            filtered = analytics.filter_by_periodicity(habits, period)
            print(f"\n--- {period.capitalize()} Habits ---")
            for h in filtered:
                print(f"[{h['id']}] {h['name']}")

        elif choice == "3":
            name = input("Enter habit name: ").strip()
            period = input("Enter periodicity (daily/weekly): ").strip().lower()
            if period not in ['daily', 'weekly']:
                print("❌ Invalid frequency choice! Use 'daily' or 'weekly'.")
                continue
            new_habit = Habit(name, period)
            if new_habit.save():
                print(f"✅ Success! '{name}' has been established.")
            else:
                print("❌ A habit with that name already exists.")

        elif choice == "4":
            cursor.execute("SELECT * FROM habits;")
            habits = analytics.get_all_habits(cursor.fetchall())
            for h in habits:
                print(f"[{h['id']}] {h['name']}")
            h_id = input("Enter the ID of the habit to check off: ").strip()
            try:
                Habit.complete_task(int(h_id))
                print("✅ Task marked complete!")
            except Exception:
                print("❌ Error processing log entry.")

        elif choice == "5":
            cursor.execute("SELECT * FROM habits;")
            habits = analytics.get_all_habits(cursor.fetchall())
            
            all_records = {}
            for h in habits:
                cursor.execute("SELECT check_in_time FROM records WHERE habit_id = ?;", (h["id"],))
                all_records[h["id"]] = [row[0] for row in cursor.fetchall()]
                
            best = analytics.extract_longest_streak_overall(habits, all_records)
            print(f"\n🏆 Peak Record: '{best['name']}' holds the longest overall streak of {best['streak']} periods!")

        elif choice == "6":
            h_id = input("Enter the Habit ID: ").strip()
            cursor.execute("SELECT periodicity, name FROM habits WHERE id = ?;", (h_id,))
            res = cursor.fetchone()
            if res:
                cursor.execute("SELECT check_in_time FROM records WHERE habit_id = ?;", (h_id,))
                records = [row[0] for row in cursor.fetchall()]
                streak = analytics.calculate_streak(records, res[0])
                print(f"🔥 The longest streak for '{res[1]}' is {streak} periods.")
            else:
                print("❌ Habit ID not found.")

        elif choice == "7":
            print("Goodbye!")
            conn.close()
            sys.exit()
        else:
            print("❌ Invalid input selection.")
            
        conn.close()

if __name__ == "__main__":
    run_menu()