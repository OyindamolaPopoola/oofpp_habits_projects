# Divinus Habit Tracker System 📊

Welcome to the **Divinus Habit Tracker System**! This is a smart, automated terminal-based application designed to help individuals and professionals track daily or weekly routines, maintain personal consistency, and view structural metrics on their tracking habits.

Whether you are tracking reading goals, workouts, or keeping an accurate record of daily business operations, this tool handles data reliably and calculates continuous streaks effortlessly.

---

## ✨ Features
* **Persistent Database Storage:** Built with an active SQLite database backend, meaning your habits and daily check-ins are saved permanently even after closing the program.
* **Smart Streak Tracking:** Advanced calculations that automatically detect exactly how many consecutive periods you successfully logged your habits, and gracefully detects when a tracking streak has been broken.
* **Pre-populated Demo History:** The software automatically generates 4 weeks of realistic historical sample data on its very first launch, letting you explore the analytical dashboards instantly.
* **Built for Reliability:** Includes an integrated unit testing architecture to ensure maximum logical accuracy and zero backend mathematical errors.

---

## 📂 Project Component Overview
* 📁 `database/` - Configures secure database connection sessions and automated database tables.
* 📁 `src/` - Contains core operational objects, data validation logic, and analytics engines.
* 📁 `tests/` - Holds individual automated test units ensuring program stability.
* 📄 `main.py` - Launches the interactive menu terminal dashboard.

---

## 🧪 How to Verify and Run Tests
If you want to run the automated validation verification suite yourself, navigate to the directory in your terminal and execute:
```bash
python -m unittest discover tests
