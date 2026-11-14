# Sports Eligibility Management System


---

## 📌 Project Overview

The **Sports Eligibility Management System** is a web-based application developed using Python and Flask to manage sports participants and automatically check their eligibility.

### Key Features
- **Dashboard:** Displays three clean summary cards:
  - Total Participants
  - Eligible Participants
  - Not Eligible Participants
- **Participant Registration:** Registration using 5 fields:
  - Participant Name
  - Age
  - Gender (`Male`, `Female`, `Other`)
  - Sports Name
  - Competition Level
- **View Participants:** Tabular display showing ONLY the required columns:
  `Participant Name | Age | Gender | Sports Name | Competition Level | Eligibility Status | Actions`
- **Actions:** Edit and Delete participant records
- **Automated Eligibility Checking:** Instant evaluation upon adding or updating participant details.

---

## 🎨 Design & Color Palette

- **Green:** `#006B54` (Primary brand color for sidebar header, table headers, buttons, eligible badges)
- **Golden Yellow:** `#C8A91F` (Accent color for borders, highlights, edit buttons)
- **Off-white:** `#F0F0E8` (Application background)
- **White:** `#FFFFFF` (Card containers, tables, and input elements)

---

## ⚖️ Eligibility Rules

Eligibility is evaluated using beginner-friendly conditional logic:

1. **Primary Level:**
   - Permitted Age: **6 to 12 years**
   - Restriction: Combat sports (*Boxing* and *Wrestling*) are **Not Eligible** at Primary Level for student safety.
2. **High School Level:**
   - Permitted Age: **13 to 18 years**
3. **Major-Competitive Level:**
   - Permitted Age: **18 to 35 years**

Participants outside these age brackets or restricted sport combinations are marked as **Not Eligible**.

---
## 🛠️ **Technologies used**

- Python
- Flask
- HTML
- CSS
- SQLite

---

## 🗄️ Database Structure (`sports_system.db`)

SQLite database table `participants`:
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Unique record ID (internal only) |
| `name` | TEXT | Participant Full Name |
| `age` | INTEGER | Age of Participant |
| `gender` | TEXT | Gender (Male, Female, Other) |
| `sport` | TEXT | Selected Sport Name |
| `level` | TEXT | Selected Competition Level |
| `eligibility`| TEXT | Automatically assigned status (`Eligible` / `Not Eligible`) |

---

## 🚀 How to Run the Project

### Option 1: One-Click Run (Windows)
Double-click `run.bat` in the project root folder.

### Option 2: Command Line
1. Open terminal in the project directory:
   ```bash
   cd "c:\mini project"
   ```
2. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

---

## 📁 Project Directory Structure

```
c:\mini project\
│
├── app.py                     # Main Flask application & routes & logic
├── database.db / sports_system.db  # SQLite database (auto-created)
├── requirements.txt           # Python dependencies
├── run.bat                    # 1-click Windows runner
├── README.md                  # Project documentation
│
├── static/
│   └── css/
│       └── style.css          # Clean custom CSS styles
│
└── templates/
    ├── base.html              # Main layout with sidebar
    ├── dashboard.html         # Dashboard with 3 cards
    ├── participants.html      # Participants table (7 columns)
    ├── add_participant.html   # 5-field registration form
    └── edit_participant.html  # 5-field edit form
```
---

## **Project Objective**
Developed as a BCA mini-project to gain practical experience in Python,Flask,SQLite and web development.
