from datetime import datetime, timedelta

def get_all_habits(db_records: list) -> list:
    """Returns a cleanly mapped list of all currently tracked habits using functional mapping."""
    return list(map(lambda x: {"id": x[0], "name": x[1], "periodicity": x[2], "created_at": x[3]}, db_records))

def filter_by_periodicity(habits_list: list, period: str) -> list:
    """Uses functional filtering to return only habits that match a specific periodicity."""
    return list(filter(lambda h: h["periodicity"] == period.lower(), habits_list))

def calculate_streak(check_in_strings: list, periodicity: str) -> int:
    """Calculates the longest consecutive running streak for a given list of check-in timestamps."""
    if not check_in_strings:
        return 0

    dates = sorted(list(set(map(lambda x: datetime.fromisoformat(x).date(), check_in_strings))))
    
    longest_streak = 0
    current_streak = 0
    previous_date = None

    for current_date in dates:
        if previous_date is None:
            current_streak = 1
        else:
            allowed_gap = 1 if periodicity == "daily" else 7
            delta = (current_date - previous_date).days

            if delta <= allowed_gap:
                if delta > 0:  
                    current_streak += 1
            else:
                current_streak = 1

        if current_streak > longest_streak:
            longest_streak = current_streak
            
        previous_date = current_date

    return longest_streak

def extract_longest_streak_overall(habits_list: list, all_records: dict) -> dict:
    """Finds the habit with the absolute longest running streak across the entire application."""
    if not habits_list:
        return {"name": "None", "streak": 0}

    streaks = list(map(lambda h: {
        "name": h["name"],
        "streak": calculate_streak(all_records.get(h["id"], []), h["periodicity"])
    }, habits_list))
    
    return max(streaks, key=lambda x: x["streak"])