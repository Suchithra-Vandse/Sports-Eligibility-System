import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "sports_eligibility_secret_key"

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sports_system.db")

# Standard Categories as per project requirements
SPORTS_LIST = [
    "Athletics",
    "Football",
    "Cricket",
    "Basketball",
    "Volleyball",
    "Badminton",
    "Swimming",
    "Kabaddi",
    "Kho-Kho",
    "Wrestling",
    "Boxing"
]

LEVELS_LIST = [
    "Primary Level",
    "High School Level",
    "Major-Competitive Level"
]

GENDER_LIST = ["Male", "Female", "Other"]


def get_db_connection():
    """Establishes connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def check_eligibility(age, level, sport):
    """
    Checks participant eligibility based on age and competition level.
    Uses simple and clear if-else conditions.
    
    Rules:
    1. Primary Level: Age 6 to 12. Combat sports (Boxing, Wrestling) not allowed.
    2. High School Level: Age 13 to 18.
    3. Major-Competitive Level: Age 18 to 35.
    """
    try:
        age = int(age)
    except (ValueError, TypeError):
        return "Not Eligible"

    # Safety rule: Boxing and Wrestling are not permitted at Primary Level
    if level == "Primary Level" and sport in ["Boxing", "Wrestling"]:
        return "Not Eligible"

    # Rule for Primary Level
    if level == "Primary Level":
        if 6 <= age <= 12:
            return "Eligible"
        else:
            return "Not Eligible"

    # Rule for High School Level
    elif level == "High School Level":
        if 13 <= age <= 18:
            return "Eligible"
        else:
            return "Not Eligible"

    # Rule for Major-Competitive Level
    elif level == "Major-Competitive Level":
        if 18 <= age <= 35:
            return "Eligible"
        else:
            return "Not Eligible"

    return "Not Eligible"


def init_db():
    """Initializes the SQLite database and creates the participants table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            sport TEXT NOT NULL,
            level TEXT NOT NULL,
            eligibility TEXT NOT NULL
        )
    """)
    conn.commit()

    # Pre-seed sample data if the table is currently empty
    cursor.execute("SELECT COUNT(*) AS count FROM participants")
    count = cursor.fetchone()["count"]
    
    if count == 0:
        sample_participants = [
            ("Rahul Sharma", 11, "Male", "Football", "Primary Level"),
            ("Priya Patel", 16, "Female", "Badminton", "High School Level"),
            ("Amit Kumar", 22, "Male", "Cricket", "Major-Competitive Level"),
            ("Sneha Reddy", 15, "Female", "Athletics", "Primary Level"),
            ("Vikram Singh", 24, "Male", "Kabaddi", "Major-Competitive Level"),
            ("Rohan Das", 10, "Male", "Boxing", "Primary Level")
        ]
        
        for name, age, gender, sport, level in sample_participants:
            status = check_eligibility(age, level, sport)
            cursor.execute("""
                INSERT INTO participants (name, age, gender, sport, level, eligibility)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, age, gender, sport, level, status))
            
        conn.commit()

    conn.close()


@app.route("/")
def dashboard():
    """Dashboard displaying summary count cards."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM participants")
    total_participants = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS eligible FROM participants WHERE eligibility = 'Eligible'")
    eligible_participants = cursor.fetchone()["eligible"]

    cursor.execute("SELECT COUNT(*) AS not_eligible FROM participants WHERE eligibility = 'Not Eligible'")
    not_eligible_participants = cursor.fetchone()["not_eligible"]

    conn.close()

    return render_template(
        "dashboard.html",
        total_participants=total_participants,
        eligible_participants=eligible_participants,
        not_eligible_participants=not_eligible_participants
    )


@app.route("/participants")
def view_participants():
    """View all registered participants in the required table format."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, gender, sport, level, eligibility FROM participants ORDER BY id DESC")
    participants = cursor.fetchall()
    conn.close()

    return render_template("participants.html", participants=participants)


@app.route("/add", methods=["GET", "POST"])
def add_participant():
    """Add a new participant with automatic eligibility check."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        sport = request.form.get("sport", "").strip()
        level = request.form.get("level", "").strip()

        # Simple validation
        if not name or not age or not gender or not sport or not level:
            flash("Please fill in all the required fields.", "error")
            return render_template(
                "add_participant.html",
                sports=SPORTS_LIST,
                levels=LEVELS_LIST,
                genders=GENDER_LIST
            )

        try:
            age_int = int(age)
            if age_int <= 0 or age_int > 120:
                flash("Please enter a valid age.", "error")
                return render_template(
                    "add_participant.html",
                    sports=SPORTS_LIST,
                    levels=LEVELS_LIST,
                    genders=GENDER_LIST
                )
        except ValueError:
            flash("Age must be a valid number.", "error")
            return render_template(
                "add_participant.html",
                sports=SPORTS_LIST,
                levels=LEVELS_LIST,
                genders=GENDER_LIST
            )

        # Automatic eligibility calculation
        eligibility = check_eligibility(age_int, level, sport)

        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO participants (name, age, gender, sport, level, eligibility)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age_int, gender, sport, level, eligibility))
        conn.commit()
        conn.close()

        flash(f"Participant '{name}' added successfully! Status: {eligibility}", "success")
        return redirect(url_for("view_participants"))

    return render_template(
        "add_participant.html",
        sports=SPORTS_LIST,
        levels=LEVELS_LIST,
        genders=GENDER_LIST
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_participant(id):
    """Edit existing participant details and recalculate eligibility."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM participants WHERE id = ?", (id,))
    participant = cursor.fetchone()

    if participant is None:
        conn.close()
        flash("Participant not found.", "error")
        return redirect(url_for("view_participants"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        sport = request.form.get("sport", "").strip()
        level = request.form.get("level", "").strip()

        if not name or not age or not gender or not sport or not level:
            flash("Please fill in all the required fields.", "error")
            conn.close()
            return render_template(
                "edit_participant.html",
                participant=participant,
                sports=SPORTS_LIST,
                levels=LEVELS_LIST,
                genders=GENDER_LIST
            )

        try:
            age_int = int(age)
            if age_int <= 0 or age_int > 120:
                flash("Please enter a valid age.", "error")
                conn.close()
                return render_template(
                    "edit_participant.html",
                    participant=participant,
                    sports=SPORTS_LIST,
                    levels=LEVELS_LIST,
                    genders=GENDER_LIST
                )
        except ValueError:
            flash("Age must be a valid number.", "error")
            conn.close()
            return render_template(
                "edit_participant.html",
                participant=participant,
                sports=SPORTS_LIST,
                levels=LEVELS_LIST,
                genders=GENDER_LIST
            )

        # Recalculate eligibility
        eligibility = check_eligibility(age_int, level, sport)

        cursor.execute("""
            UPDATE participants
            SET name = ?, age = ?, gender = ?, sport = ?, level = ?, eligibility = ?
            WHERE id = ?
        """, (name, age_int, gender, sport, level, eligibility, id))
        conn.commit()
        conn.close()

        flash(f"Participant '{name}' updated successfully! Status: {eligibility}", "success")
        return redirect(url_for("view_participants"))

    conn.close()
    return render_template(
        "edit_participant.html",
        participant=participant,
        sports=SPORTS_LIST,
        levels=LEVELS_LIST,
        genders=GENDER_LIST
    )


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_participant(id):
    """Delete a participant record from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM participants WHERE id = ?", (id,))
    participant = cursor.fetchone()

    if participant:
        name = participant["name"]
        cursor.execute("DELETE FROM participants WHERE id = ?", (id,))
        conn.commit()
        flash(f"Participant '{name}' deleted successfully.", "success")
    else:
        flash("Participant not found.", "error")

    conn.close()
    return redirect(url_for("view_participants"))


# Initialize database when module runs
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
