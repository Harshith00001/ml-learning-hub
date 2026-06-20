import streamlit as st
import pandas as pd
import json
import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent

ROADMAP_ITEMS = [
    {"Phase": "Phase 1", "Goal": "ML Fundamentals", "Outcome": "Understand core ML concepts and workflow"},
    {"Phase": "Phase 2", "Goal": "Python Data Tools & EDA", "Outcome": "Master pandas, numpy, visualization and EDA best practices"},
    {"Phase": "Phase 3", "Goal": "Scikit-Learn Core & API", "Outcome": "Estimators, transformers, pipelines and meta-estimators"},
    {"Phase": "Phase 4", "Goal": "Supervised Learning", "Outcome": "Linear models, SVM, trees, ensembles, boosting & stacking"},
    {"Phase": "Phase 5", "Goal": "Unsupervised & Representation", "Outcome": "Clustering, dimensionality reduction, manifold methods"},
    {"Phase": "Phase 6", "Goal": "Model Evaluation & Robustness", "Outcome": "Metrics, cross-val, calibration, imbalanced data"},
    {"Phase": "Phase 7", "Goal": "Production & MLOps", "Outcome": "Model persistence, serving, monitoring, reproducibility"},
    {"Phase": "Phase 8", "Goal": "Advanced / Edge Topics", "Outcome": "Time series, incremental learning, explainability"},
    {"Phase": "Phase 9", "Goal": "Deep Learning Overview", "Outcome": "When to use TF/PyTorch vs scikit-learn"}
]

LEVELS = [
    (0, "ML Explorer"),
    (500, "ML Apprentice"),
    (1200, "ML Practitioner"),
    (2200, "Scikit-Learn Specialist"),
    (3500, "ML Master")
]

BADGE_RULES = [
    ("Quiz Master", lambda stats, xp: stats['quiz_correct'] >= 10),
    ("Challenge Conqueror", lambda stats, xp: stats['challenges_completed'] >= 10),
    ("Lesson Champ", lambda stats, xp: stats['lessons_completed'] >= 15),
    ("XP Hero", lambda stats, xp: xp >= 1000),
    ("Pro Roadmap", lambda stats, xp: xp >= 2500)
]

# Badge metadata for display
BADGE_META = {
    "Quiz Master": {"icon": "📘", "desc": "Answer 10 quiz questions correctly."},
    "Challenge Conqueror": {"icon": "⚔️", "desc": "Complete 10 code challenges."},
    "Lesson Champ": {"icon": "🏅", "desc": "Complete 15 lessons."},
    "XP Hero": {"icon": "💥", "desc": "Earn 1000 XP."},
    "Pro Roadmap": {"icon": "🛣️", "desc": "Reach 2500 XP and beyond."}
}

CODE_GRADE_CHALLENGES = {
    "iris_classifier": {
        "phase": "phase5",
        "challenge_id": 3,
        "title": "Iris Logistic Regression Classifier",
        "description": "Train a logistic regression classifier on the iris dataset and print the model accuracy.",
        "starter_code": "from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import accuracy_score\n\niris = load_iris()\nX, y = iris.data, iris.target\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n# TODO: train a logistic regression classifier and print the accuracy\nmodel = LogisticRegression(max_iter=200)\nmodel.fit(X_train, y_train)\npred = model.predict(X_test)\nacc = accuracy_score(y_test, pred)\nprint(f'Accuracy: {acc:.4f}')\n",
        "target": 0.90,
        "keyword": "Accuracy",
        "xp": 150
    },
    "roc_auc_evaluator": {
        "phase": "phase6",
        "challenge_id": 2,
        "title": "ROC AUC Evaluator",
        "description": "Train a binary classifier on iris classes 0 and 1 and print ROC AUC.",
        "starter_code": "from sklearn.datasets import load_iris\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import roc_auc_score\n\ndata = load_iris()\nX = data.data[data.target != 2]\ny = data.target[data.target != 2]\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n# TODO: train a logistic regression model and print ROC AUC\nmodel = LogisticRegression(max_iter=200)\nmodel.fit(X_train, y_train)\ny_prob = model.predict_proba(X_test)[:, 1]\nauc = roc_auc_score(y_test, y_prob)\nprint(f'ROC AUC: {auc:.4f}')\n",
        "target": 0.90,
        "keyword": "ROC AUC",
        "xp": 175
    }
}

LESSON_XP = 100
PHASE_LESSON_COUNTS = {
    "phase1": 3,
    "phase2": 3,
    "phase3": 3,
    "phase4": 3,
    "phase5": 3,
    "phase6": 3,
    "phase7": 3,
    "phase8": 3,
    "phase9": 3
}

GRADE_TASK_PHASE = {
    "iris_classifier": "phase5",
    "roc_auc_evaluator": "phase6"
}

st.set_page_config(page_title="🎮 ML Learning Hub - Complete", layout="wide", initial_sidebar_state="expanded")

# ============================================
# DATABASE SETUP
# ============================================

def init_db():
    """Initialize all databases and migrate old schemas."""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()

    # Phase progress
    c.execute('''CREATE TABLE IF NOT EXISTS user_progress
                 (id INTEGER PRIMARY KEY, phase TEXT, lesson_id TEXT, 
                  completed BOOLEAN, xp INTEGER, date TEXT)''')

    # Quiz results
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_results
                 (id INTEGER PRIMARY KEY, phase TEXT, question_id INTEGER, 
                  user_answer TEXT, correct BOOLEAN, xp_earned INTEGER, date TEXT)''')

    # Code challenges
    c.execute('''CREATE TABLE IF NOT EXISTS code_challenges
                 (id INTEGER PRIMARY KEY, phase TEXT, challenge_id INTEGER, 
                  completed BOOLEAN, xp_earned INTEGER, date TEXT)''')

    # Persistent streak tracking
    c.execute('''CREATE TABLE IF NOT EXISTS activity_streak
                 (id INTEGER PRIMARY KEY, last_date TEXT UNIQUE, current_streak INTEGER, best_streak INTEGER)''')

    # Rewards table for XP bonuses (streaks, events)
    c.execute('''CREATE TABLE IF NOT EXISTS rewards
                 (id INTEGER PRIMARY KEY, date TEXT UNIQUE, xp INTEGER, reason TEXT)''')

    # Migrate old schema if needed
    def ensure_column(table, column, col_type):
        c.execute(f"PRAGMA table_info({table})")
        cols = [row[1] for row in c.fetchall()]
        if column not in cols:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

    ensure_column('user_progress', 'phase', 'TEXT')
    ensure_column('quiz_results', 'phase', 'TEXT')
    ensure_column('code_challenges', 'phase', 'TEXT')

    # Create unique indexes to prevent duplicate progress and quiz submissions
    c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_user_progress_phase_lesson ON user_progress(phase, lesson_id)')
    c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_code_challenges_phase_challenge ON code_challenges(phase, challenge_id)')
    c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_quiz_results_phase_question ON quiz_results(phase, question_id)')

    conn.commit()
    conn.close()

def save_progress(phase, lesson_id=None, status="completed", xp=0, content_type="lesson"):
    """Save lesson/challenge completion"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    
    if content_type == "lesson":
        c.execute('''INSERT OR IGNORE INTO user_progress (phase, lesson_id, completed, xp, date)
                     VALUES (?, ?, ?, ?, ?)''',
                  (phase, lesson_id, status == "completed", xp, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif content_type == "challenge":
        c.execute('''INSERT OR IGNORE INTO code_challenges (phase, challenge_id, completed, xp_earned, date)
                     VALUES (?, ?, ?, ?, ?)''',
                  (phase, lesson_id, status == "completed", xp, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    if c.rowcount > 0:
        st.session_state['total_xp'] += xp
        update_activity_streak()
    conn.commit()
    conn.close()

def save_quiz(phase, question_id, answer, correct, xp=10):
    """Save quiz result"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO quiz_results (phase, question_id, user_answer, correct, xp_earned, date)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (phase, question_id, answer, correct, xp if correct else 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # Update session state
    if correct and c.rowcount > 0:
        st.session_state['total_xp'] += xp
        update_activity_streak()
    
    conn.commit()
    conn.close()


def normalize_quiz_answer(question, selected):
    """Normalize quiz answer checks for numeric index or letter-based correct values."""
    correct = question.get('correct')
    if isinstance(correct, int):
        options = question.get('options', [])
        if 0 <= correct < len(options):
            return selected == options[correct]
        return False
    if isinstance(correct, str):
        normalized = selected.strip().upper()
        correct_letter = correct.strip().upper().rstrip(')')
        if normalized.startswith(correct_letter + ')') or normalized.startswith(correct_letter + ' '):
            return True
        if normalized == correct_letter:
            return True
        return False
    return selected == correct


def get_phase_stats(phase):
    """Get completion stats for a phase"""
    try:
        conn = sqlite3.connect('database/progress.db')
        c = conn.cursor()
        
        # Quiz stats
        c.execute('SELECT COUNT(*) FROM quiz_results WHERE phase = ?', (phase,))
        quiz_attempts = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM quiz_results WHERE phase = ? AND correct = 1', (phase,))
        quiz_correct = c.fetchone()[0]
        
        # Lesson stats
        c.execute('SELECT COUNT(*) FROM user_progress WHERE phase = ? AND completed = 1', (phase,))
        lessons_completed = c.fetchone()[0]
        
        # Challenge stats
        c.execute('SELECT COUNT(*) FROM code_challenges WHERE phase = ? AND completed = 1', (phase,))
        challenges_completed = c.fetchone()[0]
        
        conn.close()
        return {
            "quiz_attempts": quiz_attempts,
            "quiz_correct": quiz_correct,
            "lessons_completed": lessons_completed,
            "challenges_completed": challenges_completed
        }
    except Exception:
        return {
            "quiz_attempts": 0,
            "quiz_correct": 0,
            "lessons_completed": 0,
            "challenges_completed": 0
        }

def has_progress_entry(table, phase, item_id, item_column):
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute(f'SELECT COUNT(*) FROM {table} WHERE phase = ? AND {item_column} = ? AND completed = 1', (phase, item_id))
    result = c.fetchone()[0]
    conn.close()
    return result > 0


def is_lesson_complete(phase, lesson_id):
    return has_progress_entry('user_progress', phase, lesson_id, 'lesson_id')


def is_challenge_complete(phase, challenge_id):
    return has_progress_entry('code_challenges', phase, challenge_id, 'challenge_id')


def update_activity_streak():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('SELECT last_date, current_streak, best_streak FROM activity_streak ORDER BY id DESC LIMIT 1')
    row = c.fetchone()

    if row:
        last_date = datetime.strptime(row[0], '%Y-%m-%d').date()
        if last_date == today:
            conn.close()
            return row[1], row[2]
        if last_date == yesterday:
            current_streak = row[1] + 1
            best_streak = max(row[2], current_streak)
        else:
            current_streak = 1
            best_streak = max(row[2], 1)
    else:
        current_streak = 1
        best_streak = 1

    # insert new streak record
    c.execute('INSERT INTO activity_streak (last_date, current_streak, best_streak) VALUES (?, ?, ?)',
              (today.strftime('%Y-%m-%d'), current_streak, best_streak))

    # Award small XP bonus for maintaining streaks (idempotent via rewards.date unique)
    try:
        # base bonus and incremental per day
        base = 50
        incremental = 10
        bonus = base + (max(0, current_streak - 1) * incremental)
        bonus = min(bonus, 200)
        # insert reward if not already present for today
        c.execute('INSERT OR IGNORE INTO rewards (date, xp, reason) VALUES (?, ?, ?)',
                  (today.strftime('%Y-%m-%d'), bonus, f'streak_{current_streak}'))
        if c.rowcount > 0:
            # update session XP
            st.session_state['total_xp'] = st.session_state.get('total_xp', 0) + bonus
    except Exception:
        pass

    conn.commit()
    conn.close()
    return current_streak, best_streak


def get_activity_streak():
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('SELECT last_date, current_streak, best_streak FROM activity_streak ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return row[0], row[1], row[2]
    return None, 0, 0


def render_lesson_complete_button(phase, lesson_id, xp=LESSON_XP, key=None):
    completed = is_lesson_complete(phase, lesson_id)
    if completed:
        st.success(f"✅ Lesson {lesson_id} already completed")
    if st.button(f"✅ Mark Lesson {lesson_id} Complete", key=key or f"{phase}_{lesson_id}_complete", disabled=completed):
        save_progress(phase, lesson_id, "completed", xp)
        st.success(f"🎉 Lesson {lesson_id} Complete! +{xp} XP")
        st.balloons()


def render_challenge_complete_button(phase, challenge_id, xp, key=None):
    completed = is_challenge_complete(phase, challenge_id)
    if completed:
        st.success("✅ Challenge already completed")
    if st.button("✅ Mark as Complete", key=key or f"{phase}_challenge_{challenge_id}_complete", disabled=completed):
        save_progress(phase, challenge_id, "completed", xp, "challenge")
        st.success(f"Great! You earned {xp} XP!")


def load_phase_data():
    def safe_load_list(path):
        data = load_json(path)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    return value
        return []

    return {
        'phase1': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase1_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase1_challenges.json')
        },
        'phase2': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase2_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase2_challenges.json')
        },
        'phase3': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase3_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase3_challenges.json')
        },
        'phase4': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase4_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase4_challenges.json')
        },
        'phase5': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase5_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase5_challenges.json')
        },
        'phase6': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase6_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase6_challenges.json')
        },
        'phase7': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase7_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase7_challenges.json')
        },
        'phase8': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase8_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase8_challenges.json')
        },
        'phase9': {
            'questions': safe_load_list(BASE_DIR / 'challenges' / 'mcq' / 'phase9_questions.json'),
            'code': safe_load_list(BASE_DIR / 'challenges' / 'code' / 'phase9_challenges.json')
        }
    }


def get_phase_possible_xp(phase, phase_data):
    lesson_xp = PHASE_LESSON_COUNTS.get(phase, 0) * LESSON_XP
    quiz_xp = sum(q.get('xp', 0) for q in phase_data.get('questions', []))
    challenge_xp = sum(ch.get('xp', 0) for ch in phase_data.get('code', []))
    return lesson_xp + quiz_xp + challenge_xp


def get_phase_completion_ratio(phase, phase_data):
    total_xp = get_total_xp(phase)
    possible_xp = get_phase_possible_xp(phase, phase_data)
    if possible_xp == 0:
        return 0
    return int(min(100, (total_xp / possible_xp) * 100))


def get_total_xp(phase=None):
    """Calculate total XP"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    
    if phase:
        c.execute('SELECT SUM(xp_earned) FROM quiz_results WHERE correct = 1 AND phase = ?', (phase,))
        quiz_xp = c.fetchone()[0] or 0
        c.execute('SELECT SUM(xp) FROM user_progress WHERE phase = ?', (phase,))
        lesson_xp = c.fetchone()[0] or 0
        c.execute('SELECT SUM(xp_earned) FROM code_challenges WHERE completed = 1 AND phase = ?', (phase,))
        challenge_xp = c.fetchone()[0] or 0
    else:
        c.execute('SELECT SUM(xp_earned) FROM quiz_results WHERE correct = 1')
        quiz_xp = c.fetchone()[0] or 0
        c.execute('SELECT SUM(xp) FROM user_progress')
        lesson_xp = c.fetchone()[0] or 0
        c.execute('SELECT SUM(xp_earned) FROM code_challenges WHERE completed = 1')
        challenge_xp = c.fetchone()[0] or 0
    
    conn.close()
    return lesson_xp + quiz_xp + challenge_xp


def get_xp_timeline():
    """Return a cumulative XP timeline as a list of (date, cumulative_xp) pairs."""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    # collect xp by date from quiz_results, user_progress, code_challenges, rewards
    rows = {}

    c.execute("SELECT date, xp_earned FROM quiz_results WHERE correct = 1")
    for r in c.fetchall():
        d = r[0][:10]
        rows[d] = rows.get(d, 0) + (r[1] or 0)

    c.execute("SELECT date, xp FROM user_progress WHERE xp IS NOT NULL")
    for r in c.fetchall():
        d = r[0][:10]
        rows[d] = rows.get(d, 0) + (r[1] or 0)

    c.execute("SELECT date, xp_earned FROM code_challenges WHERE completed = 1")
    for r in c.fetchall():
        d = r[0][:10]
        rows[d] = rows.get(d, 0) + (r[1] or 0)

    c.execute("SELECT date, xp FROM rewards")
    for r in c.fetchall():
        d = r[0][:10]
        rows[d] = rows.get(d, 0) + (r[1] or 0)

    conn.close()
    if not rows:
        return []
    # build cumulative timeline
    dates = sorted(rows.keys())
    cum = 0
    timeline = []
    for d in dates:
        cum += rows[d]
        timeline.append((d, cum))
    return timeline


def get_next_study_recommendation():
    """Return a short recommendation for what the learner should study next."""
    # prioritize phases with incomplete lessons
    for i in range(1, 10):
        phase = f"phase{i}"
        stats = get_phase_stats(phase)
        lesson_done = stats['lessons_completed']
        lesson_total = PHASE_LESSON_COUNTS.get(phase, 0)
        if lesson_done < lesson_total:
            next_lesson = lesson_done + 1
            return f"Continue {phase.title()}: Lesson {i}.{next_lesson}"
        # if lessons complete but no quiz attempts
        if stats['quiz_attempts'] == 0:
            return f"Take the quiz for {phase.title()} to validate knowledge."
    return "All core lessons complete — try a real-world project or advanced challenge!"


def get_milestone_info(total_xp, stats):
    """Return info about next level and upcoming badge progress."""
    # Next level from existing function
    level_name, next_threshold, level_progress = get_user_level(total_xp)

    # Compute upcoming badges progress
    upcoming = []
    # Quiz Master: 10 correct
    if 'Quiz Master' not in get_badges(total_xp, stats):
        q_prog = min(100, int((stats.get('quiz_correct', 0) / 10) * 100))
        upcoming.append({'name': 'Quiz Master', 'desc': BADGE_META.get('Quiz Master', {}).get('desc',''), 'progress': q_prog})
    # Challenge Conqueror: 10 challenges
    if 'Challenge Conqueror' not in get_badges(total_xp, stats):
        c_prog = min(100, int((stats.get('challenges_completed', 0) / 10) * 100))
        upcoming.append({'name': 'Challenge Conqueror', 'desc': BADGE_META.get('Challenge Conqueror', {}).get('desc',''), 'progress': c_prog})
    # Lesson Champ: 15 lessons
    if 'Lesson Champ' not in get_badges(total_xp, stats):
        l_prog = min(100, int((stats.get('lessons_completed', 0) / 15) * 100))
        upcoming.append({'name': 'Lesson Champ', 'desc': BADGE_META.get('Lesson Champ', {}).get('desc',''), 'progress': l_prog})
    # XP-based badges
    if 'XP Hero' not in get_badges(total_xp, stats):
        xp_prog = min(100, int((total_xp / 1000) * 100))
        upcoming.append({'name': 'XP Hero', 'desc': BADGE_META.get('XP Hero', {}).get('desc',''), 'progress': xp_prog})
    if 'Pro Roadmap' not in get_badges(total_xp, stats):
        xp_prog2 = min(100, int((total_xp / 2500) * 100))
        upcoming.append({'name': 'Pro Roadmap', 'desc': BADGE_META.get('Pro Roadmap', {}).get('desc',''), 'progress': xp_prog2})

    return {
        'level_name': level_name,
        'next_threshold': next_threshold,
        'level_progress': level_progress,
        'upcoming_badges': upcoming
    }

def load_json(path):
    """Load JSON file"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def run_python_code(code):
    """Execute Python code safely and return output"""
    import subprocess
    import sys
    
    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout if result.stdout else result.stderr
        return output if output else "✅ Code executed successfully (no output)"
    except subprocess.TimeoutExpired:
        return "❌ Code execution timed out (>10 seconds)"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def parse_numeric_output(output, keyword):
    matches = re.findall(rf"{keyword}[:\s]+([0-9]*\.?[0-9]+)", output, flags=re.IGNORECASE)
    if matches:
        try:
            return float(matches[-1])
        except ValueError:
            return None
    return None


def grade_code_challenge(task_id, user_code):
    task = CODE_GRADE_CHALLENGES.get(task_id)
    if not task:
        return False, "Unknown challenge selected."

    wrapper = f"""
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

{user_code}
"""
    output = run_python_code(wrapper)
    if "Traceback" in output or "Error" in output:
        return False, output

    score = parse_numeric_output(output, task['keyword'])
    if score is None:
        return False, f"Could not parse a numeric value for {task['keyword']}. Ensure your code prints '{task['keyword']}: <value>'."

    passed = score >= task['target']
    message = f"{task['keyword']} = {score:.4f}. Target = {task['target']:.2f}."
    return passed, message

def get_user_level(total_xp):
    """Get user level, next threshold, and progress"""
    for i, (threshold, name) in enumerate(LEVELS):
        if i + 1 < len(LEVELS):
            next_threshold = LEVELS[i + 1][0]
            if total_xp < next_threshold:
                progress = int((total_xp - threshold) / (next_threshold - threshold) * 100)
                return name, next_threshold, progress
        else:
            return name, threshold, 100
    return "ML Explorer", 500, 0

def get_badges(total_xp, stats):
    """Get earned badges"""
    earned = []
    for badge_name, condition in BADGE_RULES:
        if condition(stats, total_xp):
            earned.append(badge_name)
    return earned

# ============================================
# INITIALIZE
# ============================================

init_db()
st.session_state.setdefault('total_xp', get_total_xp())

phase_data_map = load_phase_data()
phase1_data = phase_data_map['phase1']
phase2_data = phase_data_map['phase2']
phase3_data = phase_data_map['phase3']
phase4_data = phase_data_map['phase4']
phase5_data = phase_data_map['phase5']
phase6_data = phase_data_map['phase6']
phase7_data = phase_data_map['phase7']
phase8_data = phase_data_map['phase8']
phase9_data = phase_data_map['phase9']

phase1_questions = phase1_data['questions']
phase1_challenges = phase1_data['code']
phase2_questions = phase2_data['questions']
phase2_challenges = phase2_data['code']
phase3_questions = phase3_data['questions']
phase3_challenges = phase3_data['code']
phase4_questions = phase4_data['questions']
phase4_challenges = phase4_data['code']
phase5_questions = phase5_data['questions']
phase5_challenges = phase5_data['code']
phase6_questions = phase6_data['questions']
phase6_challenges = phase6_data['code']
phase7_questions = phase7_data['questions']
phase7_challenges = phase7_data['code']
phase8_questions = phase8_data['questions']
phase8_challenges = phase8_data['code']
phase9_questions = phase9_data['questions']
phase9_challenges = phase9_data['code']

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    .lesson-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .code-box {
        background-color: #f0f0f0;
        padding: 15px;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        font-family: monospace;
    }
    .syntax-highlight {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR NAVIGATION
# ============================================

st.sidebar.title("🎮 ML Learning Hub")
st.sidebar.markdown("### Complete Learning Path")

phase_select = st.sidebar.radio("📚 Select Phase:", [
    "🏠 Dashboard",
    "🧩 Real-World Projects",
    "⚙️ Setup & Deployment",
    "🟦 Phase 1: ML Fundamentals",
    "🟩 Phase 2: Python Data Tools & EDA",
    "🟪 Phase 3: Scikit-Learn Core & API",
    "🟫 Phase 4: Supervised Learning",
    "🟧 Phase 5: Unsupervised & Representation",
    "🟨 Phase 6: Model Evaluation & Robustness",
    "🟦 Phase 7: Production & MLOps",
    "🟫 Phase 8: Advanced / Edge Topics",
    "🔴 Phase 9: Deep Learning Overview",
    "📋 Scikit-Learn Checklist"
])

st.sidebar.markdown("---")
st.sidebar.metric("🏆 Total XP", f"{st.session_state['total_xp']:,}")
last_date, current_streak, best_streak = get_activity_streak()
st.sidebar.metric("🔥 Current Streak", f"{current_streak} days")
st.sidebar.metric("🥇 Best Streak", f"{best_streak} days")
st.sidebar.markdown("---")
st.sidebar.markdown("**📖 Quick Links:**")
st.sidebar.markdown("[Scikit-Learn](https://scikit-learn.org/)")
st.sidebar.markdown("[Pandas](https://pandas.pydata.org/)")
st.sidebar.markdown("[NumPy](https://numpy.org/)")

# ============================================
# MAIN DASHBOARD
# ============================================

if phase_select == "🏠 Dashboard":
    st.title("🎯 ML Learning Hub - Complete Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    total_xp = st.session_state['total_xp']
    phase_stats = [get_phase_stats(f"phase{phase_num}") for phase_num in range(1, 10)]
    phases_started = sum(1 for stats in phase_stats if stats['quiz_attempts'] + stats['lessons_completed'] + stats['challenges_completed'] > 0)
    lessons_done = sum(stats['lessons_completed'] for stats in phase_stats)
    challenges_done = sum(stats['challenges_completed'] for stats in phase_stats)
    completed_phases = sum(1 for stats in phase_stats if stats['lessons_completed'] >= 3 and stats['quiz_attempts'] > 0)
    level_name, next_threshold, progress = get_user_level(total_xp)
    agg_stats = {
        'quiz_correct': sum(stats['quiz_correct'] for stats in phase_stats),
        'challenges_completed': challenges_done,
        'lessons_completed': lessons_done
    }
    badges = get_badges(total_xp, agg_stats)
    milestones = get_milestone_info(total_xp, agg_stats)

    with col1:
        st.metric("🏆 Total XP", f"{total_xp:,}", delta=None)
    with col2:
        st.metric("📚 Phases Started", f"{phases_started}/9")
    with col3:
        st.metric("✅ Lessons Done", lessons_done)
    with col4:
        st.metric("💎 Badges", len(badges), "+ earned")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏅 Level & Progress")
        st.markdown(f"**Current Level:** {level_name}")
        if next_threshold:
            st.progress(min(progress, 100))
            st.markdown(f"**XP until next level:** {max(next_threshold - total_xp, 0)}")
        else:
            st.markdown("**Max level reached!**")
        st.markdown("**Badges:**")
        if badges:
            bcols = st.columns(max(1, min(4, len(badges))))
            for i, badge in enumerate(badges):
                meta = BADGE_META.get(badge, {})
                icon = meta.get('icon', '🏆')
                desc = meta.get('desc', '')
                with bcols[i % len(bcols)]:
                    st.markdown(f"### {icon} {badge}")
                    if desc:
                        st.caption(desc)
        else:
            st.write("No badges earned yet. Keep going!")
        # Upcoming milestones and badge progress
        st.markdown("---")
        st.markdown("**Progress to next milestones**")
        if milestones:
            # Level progress already shown; show badges
            for m in milestones['upcoming_badges']:
                st.write(f"{m['name']} — {m['desc']}")
                st.progress(min(m['progress'], 100))
    with col2:
        st.subheader("📈 Learning Progress")
        phase_ratios = [get_phase_completion_ratio(f"phase{i}", phase_data_map[f"phase{i}"]) for i in range(1, 10)]
        progress_data = {
            "Phase": [f"Phase {i}" for i in range(1, 10)],
            "Completion": phase_ratios,
            "Status": ["✅ Complete" if ratio == 100 else "🔄 In Progress" if ratio > 0 else "⭕ Not Started" for ratio in phase_ratios]
        }
        df_prog = pd.DataFrame(progress_data)
        fig = px.bar(df_prog, x="Phase", y="Completion", title="Phase Completion %", color="Status", labels={"Completion": "%"})
        st.plotly_chart(fig, use_container_width=True)

    # XP history
    timeline = get_xp_timeline()
    if timeline:
        df_xp = pd.DataFrame(timeline, columns=["date", "cumulative_xp"])
        df_xp['date'] = pd.to_datetime(df_xp['date'])
        st.subheader("📜 XP History")
        fig2 = px.line(df_xp, x='date', y='cumulative_xp', title='Cumulative XP Over Time', markers=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Phase Completion Details")
    phase_data = []
    for phase_num in range(1, 10):
        stats = phase_stats[phase_num - 1]
        phase_data.append({
            "Phase": f"Phase {phase_num}",
            "Quiz": f"{stats['quiz_correct']}/{stats['quiz_attempts']}",
            "Challenges Completed": f"{stats['challenges_completed']}",
            "Lessons Completed": f"{stats['lessons_completed']}",
            "Completion %": get_phase_completion_ratio(f"phase{phase_num}", phase_data_map[f"phase{phase_num}"])
        })
    df_stats = pd.DataFrame(phase_data)
    st.dataframe(df_stats, use_container_width=True)

    # Highlight top-level completion
    st.markdown("---")
    st.subheader("📌 Summary: Phase Progress")
    summary_cols = st.columns(3)
    total_phases_complete = sum(1 for i in range(1,10) if get_phase_completion_ratio(f"phase{i}", phase_data_map[f"phase{i}"]) == 100)
    with summary_cols[0]:
        st.metric("📦 Phases Fully Complete", f"{total_phases_complete}/9")
    with summary_cols[1]:
        st.metric("📖 Total Lessons Done", lessons_done)
    with summary_cols[2]:
        st.metric("💻 Total Challenges Done", challenges_done)

    # Next study recommendation
    st.markdown("---")
    st.subheader("🔎 What to study next")
    rec = get_next_study_recommendation()
    st.info(rec)
    
    st.markdown("---")
    st.subheader("🎯 Curriculum Roadmap")
    st.table(pd.DataFrame(ROADMAP_ITEMS))
    
    st.markdown("---")
    st.subheader("💻 Interactive Code Sandbox")
    st.markdown("Write and run Python code directly in the browser!")
    
    code_input = st.text_area(
        "Python Code Editor",
        value="# Import libraries\nimport numpy as np\nimport pandas as pd\nfrom sklearn.datasets import load_iris\n\n# Load data\niris = load_iris()\nX, y = iris.data, iris.target\n\n# Print info\nprint(f'Features: {X.shape[1]}')\nprint(f'Samples: {X.shape[0]}')\nprint(f'Classes: {len(np.unique(y))}')",
        height=200
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("▶️ Run Code"):
            with st.spinner("Running..."):
                output = run_python_code(code_input)
                st.subheader("Output:")
                st.code(output, language="text")
    with col2:
        st.info("💡 Tip: Import numpy, pandas, and sklearn libraries. Code has a 10-second timeout.")
    
    st.markdown("---")
    st.subheader("🛠️ VS Code / Anaconda / Jupyter Setup Guide")
    st.markdown("""
- Install **Anaconda** or **Miniconda** for a reliable Python environment.
- Create a new environment: `conda create -n mlhub python=3.11`
- Activate it: `conda activate mlhub`
- Install core packages: `conda install pandas numpy scikit-learn matplotlib seaborn jupyterlab`
- Install Streamlit: `pip install streamlit`
- In VS Code, install the **Python** extension and select the `mlhub` interpreter.
- For Jupyter notebooks, install `ipykernel`: `pip install ipykernel` and `python -m ipykernel install --user --name mlhub --display-name "ML Hub"`.
- Use the integrated terminal and notebooks inside VS Code for hands-on practice.
""")
    st.markdown("---")
    st.markdown("### One-Command Local Run")
    st.code("streamlit run app_main.py --server.port 8502", language="bash")
    st.markdown("Then open: http://localhost:8502")
    st.markdown("[View full setup documentation in `docs/SETUP.md`](docs/SETUP.md)")

# ============================================
# SETUP & REAL-WORLD PAGES

elif phase_select == "🧩 Real-World Projects":
    st.title("🌍 Real-World Projects")
    st.markdown("## Build portfolio-ready machine learning projects")
    st.markdown("This section helps learners translate theory into practice with end-to-end workflows.")
    st.markdown("### Project Flow")
    st.markdown("1. Define the business problem and success metrics")
    st.markdown("2. Collect and explore real datasets")
    st.markdown("3. Clean, preprocess, and engineer features")
    st.markdown("4. Train, evaluate, and tune models")
    st.markdown("5. Deploy results and create a project report or notebook")
    st.markdown("### Recommended Mini-Projects")
    st.markdown("- Customer churn prediction")
    st.markdown("- Sales forecasting with time-series data")
    st.markdown("- Image classification using transfer learning")
    st.markdown("- Fraud detection with anomaly scoring")
    st.markdown("### Learner Checklist")
    st.markdown("- [ ] Draft the problem statement")
    st.markdown("- [ ] Build a clean training pipeline")
    st.markdown("- [ ] Compare at least 2 models")
    st.markdown("- [ ] Document insights and next steps")
    st.markdown("### Real-World Tips")
    st.markdown("- Use cross-validation for robust model selection.")
    st.markdown("- Focus on explainability for stakeholders.")
    st.markdown("- Start with simple baselines before complexity.")
    st.markdown("- Keep notebooks reproducible and version controlled.")
    st.markdown("---")
    st.subheader("📂 Example Project Template")
    st.markdown("**Goal:** Predict outcomes and explain model behavior")
    st.markdown("**Tools:** `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`")
    st.markdown("**Outputs:** Cleaned dataset, model notebook, performance summary, deployment notes")
    st.markdown("---")
    st.subheader("📌 Project Readiness")
    st.markdown("Use your completed lessons, quizzes, and challenges as building blocks for project work. Real-world projects should combine data preparation, model training, evaluation, and a final summary.")

elif phase_select == "⚙️ Setup & Deployment":
    st.title("⚙️ Setup & Deployment")
    st.markdown("## Local setup, deployment notes, and documentation")
    st.markdown("### Quick Start")
    st.markdown("1. Install Python 3.11 or later.")
    st.markdown("2. Create and activate a virtual environment:")
    st.code("python -m venv .venv\n.venv\\Scripts\\activate", language="bash")
    st.markdown("3. Install required packages:")
    st.code("pip install streamlit pandas plotly scikit-learn", language="bash")
    st.markdown("4. Launch the app:")
    st.code("streamlit run app_main.py --server.port 8502", language="bash")
    st.markdown("### Deployment Notes")
    st.markdown("- Use Streamlit Cloud or a hosted Python environment for production.")
    st.markdown("- Ensure `database/progress.db` is persisted across restarts.")
    st.markdown("- Use `requirements.txt` or `environment.yml` for reproducible environments.")
    st.markdown("- Add `docs/SETUP.md` and `README.md` to your repository for contributors.")
    st.markdown("---")
    st.subheader("✅ App Health Checklist")
    st.markdown("- [ ] `app_main.py` runs without import errors")
    st.markdown("- [ ] Progress database is created automatically")
    st.markdown("- [ ] Streamlit page layout is wide and responsive")
    st.markdown("- [ ] Setup docs are available in `docs/SETUP.md`")
    st.markdown("---")
    st.markdown("### Helpful Links")
    st.markdown("- [Streamlit Documentation](https://docs.streamlit.io/)")
    st.markdown("- [SQLite Documentation](https://www.sqlite.org/docs.html)")
    st.markdown("- [scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)")
# ============================================

elif phase_select == "🟦 Phase 1: ML Fundamentals":
    st.title("🟦 Phase 1: ML Fundamentals")
    phase1_page = st.sidebar.radio("Phase 1:", [
        "Overview",
        "Lesson 1.1",
        "Lesson 1.2",
        "Lesson 1.3",
        "Quiz",
        "Code Challenges"
    ])
    if phase1_page == "Overview":
        st.markdown("""
        ## Phase 1: ML Fundamentals
        
        Learn the core concepts of machine learning from scratch.
        
        **Topics:**
        - What is Machine Learning?
        - Types of ML (Supervised, Unsupervised, Reinforcement)
        - Key Concepts (Features, Target, Train-Test Split, Overfitting)
        """)
        progress_df = pd.DataFrame({
            "Lesson": ["1.1 What is ML", "1.2 Types of ML", "1.3 Key Concepts"],
            "Status": ["✅", "✅", "✅"]
        })
        st.table(progress_df)
    elif phase1_page == "Lesson 1.1":
        st.header("📚 Lesson 1.1: What is Machine Learning?")
        tabs = st.tabs(["📖 Content", "💡 Examples", "✅ Complete"])
        with tabs[0]:
            st.markdown("""
## What is Machine Learning?

**Definition:** Machine Learning is the field of computer science that enables systems to learn and improve from data without being explicitly programmed.

### Key Difference: Traditional vs ML

**Traditional Programming:**
```
Rules (Hardcoded) + Data → Program → Output
```
- Programmer writes every rule manually
- Not adaptable to new patterns
- Example: Spam filter with 100+ hardcoded rules

**Machine Learning:**
```
Data + Output Examples → Algorithm → Learned Rules → Model
```
- Algorithm discovers rules automatically
- Adapts to new patterns
- Example: Spam filter learns from examples

### Real-World Applications

- 📧 Email spam detection
- 🎬 Netflix recommendations
- 🗣️ Voice assistants (Siri, Alexa)
- 🚗 Autonomous vehicles
- 🏥 Medical diagnosis
- 💰 Fraud detection
- 📱 Face recognition
            """)
        with tabs[1]:
            st.markdown("""
### Example 1: Spam Detection

**Traditional Way:**
```python
if "Buy now!" in email:
    return "SPAM"
if "Click here" in email:
    return "SPAM"
if "Limited time" in email:
    return "SPAM"
# ... hundreds more rules!
```

**Machine Learning Way:**
```python
# Train on examples
spam_emails = [email1, email2, ...]
not_spam_emails = [email3, email4, ...]

model.fit(all_emails, labels)

prediction = model.predict(new_email)
```
            """)
        with tabs[2]:
            render_lesson_complete_button("phase1", "1.1", 100, key="p1_lesson1_complete")
    elif phase1_page == "Lesson 1.2":
        st.header("📚 Lesson 1.2: Three Types of Machine Learning")
        tabs = st.tabs(["📖 Content", "📊 Comparison", "💻 Code", "✅ Complete"])
        with tabs[0]:
            st.markdown("""
## Three Types of Machine Learning

### 1️⃣ Supervised Learning
**Learning from labeled data**

### 2️⃣ Unsupervised Learning
**Finding patterns in unlabeled data**

### 3️⃣ Reinforcement Learning
**Learning through rewards and penalties**
            """)
        with tabs[1]:
            comparison = pd.DataFrame({
                "Aspect": ["Data Type", "Labels", "Goal", "Learning Style"],
                "Supervised": ["Labeled pairs (X, y)", "Yes ✅", "Predict specific values", "Learn mapping"],
                "Unsupervised": ["Unlabeled (X only)", "No ❌", "Discover patterns", "Explore structure"],
                "Reinforcement": ["Experiences/States", "N/A", "Maximize rewards", "Trial & error"]
            })
            st.table(comparison)
        with tabs[2]:
            st.markdown("""
**Supervised (Classification):**
```python
from sklearn.tree import DecisionTreeClassifier
X = [[2000, 3], [1500, 2], [3000, 4]]
y = ['Expensive', 'Cheap', 'Expensive']
model = DecisionTreeClassifier()
model.fit(X, y)
prediction = model.predict([[2500, 3]])
```
            """)
        with tabs[3]:
            render_lesson_complete_button("phase1", "1.2", 100, key="p1_lesson2_complete")
    elif phase1_page == "Lesson 1.3":
        st.header("📚 Lesson 1.3: Key Concepts & Terminology")
        tabs = st.tabs(["📖 Content", "🔍 Deep Dive", "📊 Visual", "✅ Complete"])
        with tabs[0]:
            st.markdown("""
## Key Concepts Every Beginner Needs

### Features (X) and Target (y)

```python
X = [[2000, 3, 2], [1500, 2, 1], [3000, 4, 3]]
y = [500000, 350000, 650000]
```
            """)
        with tabs[1]:
            st.markdown("""
### Overfitting vs Underfitting

- Overfitting: high train accuracy, low test accuracy
- Underfitting: low accuracy on both
            """)
        with tabs[2]:
            epochs = list(range(1, 21))
            train_loss = [0.9 - (0.85 * (i/20)**1.5) for i in range(1, 21)]
            test_loss = [0.9 - (0.8 * (i/20)**1.3) + 0.02 * ((i-15)/5)**2 if i > 15 else 0.9 - (0.8 * (i/20)**1.3) for i in range(1, 21)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=epochs, y=train_loss, mode='lines+markers', name='Training Loss', line=dict(color='green', width=3)))
            fig.add_trace(go.Scatter(x=epochs, y=test_loss, mode='lines+markers', name='Test Loss', line=dict(color='red', width=3)))
            fig.update_layout(title="Overfitting Example: Training vs Test Loss", xaxis_title="Epoch", yaxis_title="Loss", hovermode='x unified', template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        with tabs[3]:
            render_lesson_complete_button("phase1", "1.3", 100, key="p1_lesson3_complete")
    elif phase1_page == "Quiz":
        st.header("❓ Phase 1 Quiz")
        questions = load_json('challenges/mcq/phase1_questions.json').get('phase1_fundamentals', [])
        if questions:
            for idx, q in enumerate(questions[:3], 1):
                st.markdown(f"### Question {idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p1_q{q['id']}")
                if st.button("Submit", key=f"p1_submit_{q['id']}"):
                    correct = selected == q["options"][q["correct"]]
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        save_quiz("phase1", q['id'], selected, True, q['xp'])
                    else:
                        st.error("❌ Incorrect")
                    st.info(f"📝 {q['explanation']}")
                st.markdown("---")
        else:
            st.info("No Phase 1 quiz questions found yet.")
    elif phase1_page == "Code Challenges":
        st.header("💻 Phase 1 Code Challenges")
        challenges = load_json('challenges/code/phase1_challenges.json').get('phase1_code_challenges', [])
        if challenges:
            for challenge in challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p1_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase1", challenge['id'], challenge.get('xp', 100), key=f"p1_complete_{challenge['id']}")
        else:
            st.info("No Phase 1 code challenges found yet.")

# ============================================
# PHASE 2: SCIKIT-LEARN BASICS
# ============================================

elif phase_select == "🟩 Phase 2: Python Data Tools & EDA":
    st.title("🟩 Phase 2: Python Data Tools & EDA")
    st.info("📊 Master pandas, numpy, visualization, and EDA fundamentals for ML.")
    
    phase2_page = st.sidebar.radio("Phase 2:", [
        "Overview",
        "Lesson 2.1: pandas",
        "Lesson 2.2: NumPy & Visualization",
        "Lesson 2.3: EDA & Data Cleaning",
        "Quiz",
        "Code Challenges"
    ])
    
    if phase2_page == "Overview":
        st.markdown("""
        ## Phase 2: Python Data Tools & EDA
        
        **Objective:** Master essential Python tools for data analysis and exploration.
        
        ### What You'll Learn:
        - **pandas**: DataFrames, filtering, grouping, merging
        - **NumPy**: Arrays, vectorization, broadcasting
        - **Visualization**: matplotlib, seaborn for exploratory plots
        - **EDA**: Identifying patterns, anomalies, and data quality issues
        - **Data Cleaning**: Handling missing values, outliers, duplicates
        
        ### Why It Matters:
        **80% of ML is data preparation!** These tools enable fast, efficient data exploration and cleaning.
        
        ### Prerequisites:
        - Phase 1: ML Fundamentals
        
        ### Outcomes:
        ✅ Load and explore datasets efficiently
        ✅ Transform and clean messy data
        ✅ Identify patterns and correlations
        ✅ Create publication-quality visualizations
        ✅ Prepare clean data for modeling
        """)
        
        with st.expander("📚 Tools Overview"):
            st.markdown("""
            | Tool | Purpose | Key Method |
            |------|---------|-----------|
            | **pandas** | Data manipulation & analysis | `.groupby()`, `.merge()`, `.describe()` |
            | **NumPy** | Numerical computing | `.mean()`, `.std()`, broadcasting |
            | **matplotlib** | Low-level plotting | `.plot()`, `.scatter()`, `.histogram()` |
            | **seaborn** | Statistical visualization | `.heatmap()`, `.boxplot()`, `.stripplot()` |
            """)
    
    elif phase2_page == "Lesson 2.1: pandas":
        st.subheader("Lesson 2.1: pandas — Data Manipulation Powerhouse")
        
        st.markdown("""
        ### What is pandas?
        
        pandas provides **DataFrames** (2D tables) and **Series** (1D arrays) for data manipulation.
        It's the go-to tool for loading, cleaning, and transforming data.
        
        ### Core Concepts
        
        **Series**: 1D labeled array
        ```python
        import pandas as pd
        s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
        print(s['a'])  # 1
        ```
        
        **DataFrame**: 2D labeled table (rows × columns)
        ```python
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [50000, 60000, 75000]
        })
        ```
        """)
        
        st.markdown("### Loading & Exploring Data")
        st.code("""import pandas as pd

# Load from CSV
df = pd.read_csv('data.csv')

# First/last rows
print(df.head())      # First 5 rows
print(df.tail())      # Last 5 rows

# Shape and info
print(df.shape)       # (rows, columns)
print(df.info())      # Dtypes, non-null counts
print(df.describe())  # Statistics (mean, std, min, max)""", language='python')
        
        st.markdown("### Filtering & Selection")
        st.code("""# Column selection
salary = df['salary']
subset = df[['name', 'salary']]

# Row filtering
young = df[df['age'] < 30]
high_earners = df[df['salary'] > 60000]

# Combining conditions
df[(df['age'] < 30) & (df['salary'] > 50000)]

# Using .loc (label-based)
df.loc[df['name'] == 'Alice', 'salary']

# Using .iloc (position-based)
df.iloc[0, 1]  # First row, second column""", language='python')
        
        st.markdown("### Grouping & Aggregation")
        st.code("""# Group by and aggregate
by_dept = df.groupby('department')['salary'].mean()

# Multiple aggregations
summary = df.groupby('department').agg({
    'salary': ['mean', 'min', 'max'],
    'age': 'mean'
})

# Custom aggregations
df.groupby('department').apply(lambda x: x['salary'].max() - x['salary'].min())""", language='python')
        
        st.markdown("### Merging & Joining")
        st.code("""# Inner join (only matching rows)
merged = pd.merge(df1, df2, on='id', how='inner')

# Left join (keep all from left)
merged = df1.merge(df2, on='id', how='left')

# Concatenate (stack vertically)
combined = pd.concat([df1, df2], axis=0)

# Combine (side-by-side)
combined = pd.concat([df1, df2], axis=1)""", language='python')
        
        st.markdown("### Handling Missing Values")
        st.code("""# Check for missing values
print(df.isnull().sum())

# Drop rows with any missing
df_clean = df.dropna()

# Drop columns with too many missing
df_clean = df.dropna(thresh=len(df)*0.8, axis=1)

# Fill missing with value
df['age'] = df['age'].fillna(df['age'].median())

# Forward/backward fill
df['value'].fillna(method='ffill')  # Forward fill""", language='python')
        
        render_lesson_complete_button("phase2", "lesson_2_1_pandas", 200, key="p2_l21")
    
    elif phase2_page == "Lesson 2.2: NumPy & Visualization":
        st.subheader("Lesson 2.2: NumPy & Visualization — Computing & Plotting")
        
        st.markdown("""
        ### NumPy Fundamentals
        
        NumPy provides fast **n-dimensional arrays** and vectorized operations.
        
        **Why NumPy over lists?**
        - 50-100x faster (vectorized C operations)
        - Broadcasting for element-wise operations
        - Memory efficient
        """)
        
        st.code("""import numpy as np

# Create arrays
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2], [3, 4]])

# Special arrays
zeros = np.zeros((3, 4))
ones = np.ones(5)
range_arr = np.arange(0, 10, 2)  # 0, 2, 4, 6, 8
linspace = np.linspace(0, 1, 11)  # 11 evenly spaced

# Shape and reshape
arr.shape  # (5,)
arr.reshape(1, 5)
arr.reshape(-1, 1)  # Auto-calculate dimension""", language='python')
        
        st.markdown("### Vectorized Operations (Broadcasting)")
        st.code("""# Element-wise operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

c = a + b  # [5, 7, 9]
c = a * b  # [4, 10, 18]
c = a ** 2  # [1, 4, 9]

# Broadcasting (automatic expansion)
matrix = np.array([[1, 2], [3, 4]])
matrix + 10  # Adds 10 to every element

# Operations across axes
mean_rows = matrix.mean(axis=0)  # Mean per column
mean_cols = matrix.mean(axis=1)  # Mean per row""", language='python')
        
        st.markdown("### Visualization with matplotlib")
        st.code("""import matplotlib.pyplot as plt

# Line plot
plt.figure(figsize=(10, 5))
plt.plot(x, y, label='Line 1')
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.legend()
plt.show()

# Scatter plot
plt.scatter(x, y, alpha=0.5, s=50)

# Histogram
plt.hist(data, bins=30, edgecolor='black')

# Multiple subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(x, y)
axes[1].scatter(x, y)""", language='python')
        
        st.markdown("### Statistical Visualization with seaborn")
        st.code("""import seaborn as sns
import matplotlib.pyplot as plt

# Heatmap (correlation matrix)
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')

# Box plot (distribution by category)
sns.boxplot(data=df, x='category', y='value')

# Violin plot (distribution shape)
sns.violinplot(data=df, x='category', y='value')

# Strip plot (scatter for categorical)
sns.stripplot(data=df, x='category', y='value', jitter=True)

# Pair plot (all pairwise relationships)
sns.pairplot(df, hue='target')""", language='python')
        
        st.markdown("### Common Plotting Patterns for EDA")
        st.code("""# Distribution of single variable
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].hist(df['column'])  # Histogram
axes[1].boxplot(df['column'])  # Box plot
axes[2].hist(np.log1p(df['column']), bins=30)  # Log scale

# Correlation matrix
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

# Distributions by group
for group in df['category'].unique():
    subset = df[df['category'] == group]['value']
    plt.hist(subset, alpha=0.5, label=group, bins=20)
plt.legend()""", language='python')
        
        render_lesson_complete_button("phase2", "lesson_2_2_numpy_viz", 200, key="p2_l22")
    
    elif phase2_page == "Lesson 2.3: EDA & Data Cleaning":
        st.subheader("Lesson 2.3: EDA & Data Cleaning — Preparing Data for ML")
        
        st.markdown("""
        ### Exploratory Data Analysis (EDA) Workflow
        
        EDA helps you understand your data **before building models**.
        
        **Key questions EDA answers:**
        - What are the distributions of variables?
        - What patterns exist in the data?
        - Which variables are correlated?
        - Are there outliers or anomalies?
        - How much missing data is there?
        """)
        
        st.code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load and inspect
df = pd.read_csv('data.csv')
print(f"Shape: {df.shape}")
print(df.head())
print(df.info())
print(df.describe())

# 2. Check for missing
print(df.isnull().sum())
print((df.isnull().sum() / len(df) * 100).round(2))  # % missing

# 3. Check for duplicates
print(f"Duplicates: {df.duplicated().sum()}")

# 4. Identify data types
print(df.dtypes)""", language='python')
        
        st.markdown("### Handling Missing Values")
        st.code("""# Strategy 1: Drop rows
df_clean = df.dropna(subset=['important_column'])

# Strategy 2: Drop columns (too sparse)
df_clean = df.dropna(thresh=len(df)*0.7, axis=1)  # Keep 70% non-null

# Strategy 3: Fill with central tendency
df['age'].fillna(df['age'].median(), inplace=True)
df['category'].fillna(df['category'].mode()[0], inplace=True)

# Strategy 4: Forward/backward fill (time series)
df['value'].fillna(method='ffill', inplace=True)

# Strategy 5: Interpolation
df['value'].interpolate(method='linear', inplace=True)""", language='python')
        
        st.markdown("### Detecting & Handling Outliers")
        st.code("""# 1. Statistical method (z-score)
from scipy import stats
z_scores = np.abs(stats.zscore(df['value']))
outliers = df[z_scores > 3]

# 2. IQR method
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['value'] < Q1 - 1.5*IQR) | (df['value'] > Q3 + 1.5*IQR)]

# Remove or cap outliers
df_clean = df[(df['value'] >= Q1 - 1.5*IQR) & (df['value'] <= Q3 + 1.5*IQR)]

# Cap outliers (replace with boundary)
df['value'] = df['value'].clip(lower=Q1 - 1.5*IQR, upper=Q3 + 1.5*IQR)""", language='python')
        
        st.markdown("### Feature Engineering for EDA")
        st.code("""# 1. Create new columns
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 100], labels=['teen', 'young', 'mid', 'senior'])

# 2. Encode categorical
df['gender_encoded'] = (df['gender'] == 'M').astype(int)
df = pd.get_dummies(df, columns=['category'], drop_first=True)

# 3. Transform skewed distributions
df['log_income'] = np.log1p(df['income'])
df['sqrt_value'] = np.sqrt(df['value'])

# 4. Scaling (standardization)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['value_scaled'] = scaler.fit_transform(df[['value']])""", language='python')
        
        st.markdown("### End-to-End EDA Example")
        st.code("""import pandas as pd
import numpy as np

# Load
df = pd.read_csv('sales.csv')

# 1. Basic stats
print(f"Shape: {df.shape}, Missing: {df.isnull().sum().sum()}")

# 2. Distribution analysis
print(df.describe())

# 3. Correlation
print(df.corr())

# 4. Find outliers
for col in df.select_dtypes(include=[np.number]).columns:
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    outlier_count = ((df[col] < Q1 - 1.5*(Q3-Q1)) | (df[col] > Q3 + 1.5*(Q3-Q1))).sum()
    print(f"{col}: {outlier_count} outliers")

# 5. Clean
df = df.dropna()
df = df[~df.duplicated()]

print(f"After cleaning: {df.shape}")""", language='python')
        
        render_lesson_complete_button("phase2", "lesson_2_3_eda_cleaning", 200, key="p2_l23")
    
    elif phase2_page == "Quiz":
        st.subheader("Phase 2 Quiz: pandas, NumPy, Visualization & EDA")
        
        try:
            with open('challenges/mcq/phase2_questions.json', 'r') as f:
                phase2_questions = json.load(f)
        except:
            st.error("Phase 2 quiz file not found.")
            phase2_questions = []
        
        if phase2_questions:
            for i, q in enumerate(phase2_questions):
                st.markdown(f"### Question {i+1}: {q['question']}")
                selected = st.radio(f"Choose answer (Q{i+1}):", q['options'], key=f"p2_q{i}")
                
                if st.button(f"Check (Q{i+1})", key=f"p2_check_q{i}"):
                    if selected == q['correct']:
                        st.success(f"✅ Correct! +{q.get('xp', 50)} XP")
                        save_quiz_result(f"phase2_q{i}", True, q.get('xp', 50))
                    else:
                        st.error(f"❌ Incorrect. Correct answer: {q['correct']}")
                        st.info(f"💡 {q['explanation']}")
                        save_quiz_result(f"phase2_q{i}", False, 0)
                st.divider()
        else:
            st.warning("No quiz questions available for Phase 2 yet.")
    
    elif phase2_page == "Code Challenges":
        st.subheader("Phase 2 Code Challenges")
        
        try:
            with open('challenges/code/phase2_challenges.json', 'r') as f:
                phase2_challenges = json.load(f)
        except:
            st.error("Phase 2 code challenges file not found.")
            phase2_challenges = []
        
        if phase2_challenges:
            challenge_select = st.selectbox(
                "Select a challenge:",
                [c['title'] for c in phase2_challenges],
                key="p2_challenge_select"
            )
            
            challenge = next((c for c in phase2_challenges if c['title'] == challenge_select), None)
            if challenge:
                st.markdown(f"**Difficulty:** {challenge['difficulty']}")
                st.markdown(challenge['description'])
                
                st.markdown("**Starter Code:**")
                st.code(challenge.get('starter_code', "# Write your solution here"), language='python')
                
                user_code = st.text_area("Your Solution:", height=200, key=f"p2_code_{challenge['id']}")
                
                if st.button("Run & Test", key=f"p2_run_{challenge['id']}"):
                    result = grade_code_challenge(user_code, challenge.get('solution', ''), challenge['id'])
                    if result['passed']:
                        st.success(f"✅ Challenge completed! +{challenge.get('xp', 100)} XP")
                        render_challenge_complete_button("phase2", challenge['id'], challenge.get('xp', 100), key=f"p2_complete_{challenge['id']}")
                    else:
                        st.error(f"❌ Tests failed: {result['error']}")
                        if challenge.get('hints'):
                            with st.expander("💡 Hint"):
                                st.markdown(challenge['hints'][0] if isinstance(challenge['hints'], list) else challenge['hints'])
        else:
            st.info("No code challenges available for Phase 2 yet.")

# ============================================
# PHASE 3: SCIKIT-LEARN CORE & API
# ============================================

elif phase_select == "🟪 Phase 3: Scikit-Learn Core & API":
    st.title("🟪 Phase 3: Scikit-Learn Core & API")
    st.info("🔧 Master pipelines, ColumnTransformer, hyperparameter tuning, and production-ready patterns.")
    
    phase3_page = st.sidebar.radio("Phase 3:", [
        "Overview",
        "Lesson 3.1: Pipelines",
        "Lesson 3.2: ColumnTransformer",
        "Lesson 3.3: GridSearchCV",
        "Quiz",
        "Code Challenges"
    ])
    
    if phase3_page == "Overview":
        st.markdown("""
        ## Phase 3: Scikit-Learn Core & API
        
        **Objective:** Understand and master the foundational APIs that enable professional ML workflows.
        
        ### What You'll Learn:
        - **Pipelines**: Chain estimators for seamless preprocessing + modeling
        - **ColumnTransformer**: Handle mixed feature types (numeric, categorical) elegantly
        - **GridSearchCV**: Systematically search hyperparameter spaces
        - **Custom Estimators**: Build domain-specific transformers and models
        
        ### Why It Matters:
        Pipelines and ColumnTransformer prevent **data leakage** and make code **reproducible**.
        GridSearchCV finds optimal hyperparameters automatically.
        These are **non-negotiable** for production ML systems.
        
        ### Prerequisites:
        - Phase 1: ML Fundamentals
        - Phase 2: Python Data Tools & EDA
        
        ### Outcomes:
        ✅ Build preprocessing pipelines
        ✅ Handle mixed feature types with ColumnTransformer
        ✅ Perform hyperparameter search with GridSearchCV
        ✅ Understand fit/transform/fit_transform semantics
        ✅ Deploy reproducible models
        """)
        
        with st.expander("📚 Key Concepts at a Glance"):
            st.markdown("""
            | Concept | Purpose | Key Method |
            |---------|---------|-----------|
            | **Pipeline** | Chain steps (fit all, predict once) | `.fit()` / `.predict()` |
            | **ColumnTransformer** | Apply different transformers to different column groups | `.fit_transform()` |
            | **GridSearchCV** | Search hyperparameter grid exhaustively | `.best_params_` |
            | **Cross-Validation** | Prevent overfitting via k-fold splits | `cv=5` |
            """)
    
    elif phase3_page == "Lesson 3.1: Pipelines":
        st.subheader("Lesson 3.1: Pipelines — Chaining Estimators")
        
        st.markdown("""
        ### What is a Pipeline?
        A `Pipeline` chains multiple estimators (transformers + final estimator) into a single object.
        
        **Key Benefits:**
        - Prevents **data leakage** (fit transformers on train only)
        - Simplifies code (one `fit()` call chains all steps)
        - Ensures reproducibility (same preprocessing always applied)
        - Deployable as single object
        
        ### The Problem It Solves
        
        **❌ WITHOUT Pipeline (data leakage risk):**
        ```python
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)  # PROBLEM: Fit on ALL data!
        X_train, X_test = train_test_split(X_scaled, ...)  # Split AFTER scaling
        model = LogisticRegression()
        model.fit(X_train, y_train)  # Test leakage possible
        ```
        
        **✅ WITH Pipeline (correct):**
        ```python
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression())
        ])
        X_train, X_test = train_test_split(X, y)
        pipeline.fit(X_train, y_train)  # Scaler fit only on train!
        y_pred = pipeline.predict(X_test)
        ```
        
        ### Anatomy of a Pipeline
        """)
        
        st.markdown("""
        ```
        Pipeline([
            ('step1_name', Transformer1()),   # fit + transform
            ('step2_name', Transformer2()),   # fit + transform  
            ('step3_name', FinalEstimator())  # only fit (no transform)
        ])
        ```
        
        - All steps except the last **must have `transform()`**
        - The last step can be transformer (for unsupervised) or estimator (for supervised)
        - Names are arbitrary but should be descriptive
        """)
        
        st.code("""from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Example 1: Simple 2-step pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)""", language='python')
        
        st.markdown("### Example 2: Multi-Step Pipeline with Feature Engineering")
        st.code("""from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

pipe = Pipeline([
    ('poly_features', PolynomialFeatures(degree=2)),
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=10)),
    ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Fit entire pipeline
pipe.fit(X_train, y_train)

# Predict (all transformations applied automatically)
y_pred = pipe.predict(X_test)
print(f"Accuracy: {pipe.score(X_test, y_test)}")""", language='python')
        
        st.markdown("### Accessing Pipeline Components")
        st.code("""# Get a specific step by name
scaler = pipe.named_steps['scaler']
print(scaler.scale_)  # Access fitted parameters

# Get parameters
print(pipe.get_params())

# Set parameters (useful for GridSearchCV)
pipe.set_params(pca__n_components=20, rf__n_estimators=200)""", language='python')
        
        st.markdown("### Key Insight: Fit/Transform Semantics")
        with st.expander("🧠 Understanding fit() vs transform() vs fit_transform()"):
            st.markdown("""
            - **`.fit(X)`**: Learn parameters from X (e.g., mean/std for scaler)
            - **`.transform(X)`**: Apply learned transformation to X
            - **`.fit_transform(X)`**: Combination of both (more efficient)
            
            **In a pipeline:**
            - `pipe.fit(X_train, y_train)` calls `fit` on all steps, `fit_transform` on transformers
            - `pipe.predict(X_test)` calls `transform` on all steps, then `predict` on final estimator
            """)
        
        render_lesson_complete_button("phase3", "lesson_3_1_pipelines", 200, key="p3_l31")
    
    elif phase3_page == "Lesson 3.2: ColumnTransformer":
        st.subheader("Lesson 3.2: ColumnTransformer — Mixed Feature Types")
        
        st.markdown("""
        ### The Problem: Different Features, Different Treatment
        
        Real datasets have **mixed types**:
        - Numeric: age, income, score (need scaling)
        - Categorical: color, country, category (need encoding)
        
        **Without ColumnTransformer:**
        ```python
        X_numeric = X[['age', 'income']].apply(StandardScaler())
        X_cat = pd.get_dummies(X[['color', 'country']])
        X_processed = pd.concat([X_numeric, X_cat], axis=1)  # Messy!
        ```
        
        **With ColumnTransformer:**
        ```python
        ct = ColumnTransformer([
            ('numeric', StandardScaler(), ['age', 'income']),
            ('categoric', OneHotEncoder(), ['color', 'country'])
        ])
        X_processed = ct.fit_transform(X)  # Clean!
        ```
        """)
        
        st.markdown("### ColumnTransformer Syntax")
        st.code("""from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

ct = ColumnTransformer([
    ('step1_name', Transformer1(), [col1, col2, ...]),
    ('step2_name', Transformer2(), [col3, col4, ...])
])

# Apply to data
X_transformed = ct.fit_transform(X)
""", language='python')
        
        st.markdown("### Example: Comprehensive Mixed-Type Pipeline")
        st.code("""import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Sample data
X = pd.DataFrame({
    'age': [25, 45, 35, 55],
    'income': [30000, 80000, 50000, 120000],
    'gender': ['M', 'F', 'M', 'F'],
    'country': ['USA', 'UK', 'USA', 'CA']
})

# Define transformations
ct = ColumnTransformer([
    ('numeric', StandardScaler(), ['age', 'income']),
    ('categoric', OneHotEncoder(sparse_output=False, drop='first'), ['gender', 'country'])
])

# Full pipeline
pipe = Pipeline([
    ('preprocessor', ct),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Use it
pipe.fit(X, y)
y_pred = pipe.predict(X_test)""", language='python')
        
        st.markdown("### Advanced: Using make_column_selector")
        st.code("""from sklearn.compose import make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder

ct = ColumnTransformer([
    ('numeric', StandardScaler(), make_column_selector(dtype_include=['int64', 'float64'])),
    ('categoric', OneHotEncoder(), make_column_selector(dtype_include=['object']))
])
""", language='python')
        
        st.markdown("### Best Practices")
        with st.expander("✅ ColumnTransformer Best Practices"):
            st.markdown("""
            1. **Always use within Pipeline** to prevent data leakage
            2. **Order transformers** (numeric first, then categorical) for clarity
            3. **Use `remainder='passthrough'`** if some columns should be untransformed
            4. **Validate dtypes** of your DataFrame before ColumnTransformer
            5. **Test on a sample** first to ensure correct column selection
            """)
        
        render_lesson_complete_button("phase3", "lesson_3_2_columntransformer", 200, key="p3_l32")
    
    elif phase3_page == "Lesson 3.3: GridSearchCV":
        st.subheader("Lesson 3.3: GridSearchCV — Hyperparameter Tuning")
        
        st.markdown("""
        ### What Are Hyperparameters?
        
        **Hyperparameters** are settings you choose BEFORE fitting (not learned from data):
        - Random Forest: `n_estimators`, `max_depth`, `min_samples_split`
        - SVM: `C`, `kernel`, `gamma`
        - KNN: `n_neighbors`, `metric`, `weights`
        
        **Question:** How do you choose optimal values?
        **Answer:** GridSearchCV searches exhaustively over a parameter grid!
        """)
        
        st.markdown("### GridSearchCV Workflow")
        st.code("""from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Define hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

# Create GridSearchCV
grid = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='accuracy',
    n_jobs=-1  # Use all CPU cores
)

# Fit (tries all combinations)
grid.fit(X_train, y_train)

# Best results
print(f"Best params: {grid.best_params_}")
print(f"Best CV score: {grid.best_score_}")
print(f"Test score: {grid.score(X_test, y_test)}")

# Best model ready to use
y_pred = grid.predict(X_test)
""", language='python')
        
        st.markdown("### Example: GridSearchCV with Pipeline")
        st.code("""from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC())
])

# Hyperparameters with pipeline step prefixes
param_grid = {
    'svc__C': [0.1, 1, 10],
    'svc__kernel': ['linear', 'rbf'],
    'svc__gamma': ['scale', 'auto']
}

grid = GridSearchCV(pipe, param_grid, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)

print(grid.best_estimator_)  # Full fitted pipeline
""", language='python')
        
        st.markdown("### RandomizedSearchCV for Large Grids")
        st.code("""from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

# For LARGE grids, RandomizedSearchCV samples randomly (faster!)
param_dist = {
    'n_estimators': randint(50, 500),
    'max_depth': randint(3, 20),
    'min_samples_split': randint(2, 20)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(),
    param_dist,
    n_iter=20,  # Try 20 random combinations
    cv=5,
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train, y_train)
""", language='python')
        
        st.markdown("### Visualizing GridSearchCV Results")
        st.code("""import pandas as pd

# Get results as DataFrame
results_df = pd.DataFrame(grid.cv_results_)

# View top parameters
best_results = results_df.nlargest(5, 'mean_test_score')[
    ['params', 'mean_test_score', 'std_test_score']
]
print(best_results)

# Plot: Number of estimators vs Score
import matplotlib.pyplot as plt
results_df.plot(x='params.n_estimators', y='mean_test_score', kind='scatter')
plt.show()
""", language='python')
        
        st.markdown("### Key Hyperparameter Tips")
        with st.expander("🎯 GridSearch Best Practices"):
            st.markdown("""
            1. **Start broad, then narrow**: First grid with wide ranges, then zoom in
            2. **Use cross-validation**: `cv=5` or `cv=StratifiedKFold(n_splits=5)`
            3. **Use `n_jobs=-1`**: Parallelize across all cores
            4. **Monitor time**: Large grids can take hours; use `RandomizedSearchCV` for large spaces
            5. **Look at top-5**: Sometimes difference between best params is negligible
            6. **Always test on held-out test set**: `grid.score(X_test, y_test)`
            7. **Consider nested CV**: Outer for evaluation, inner for hyperparameter tuning
            """)
        
        render_lesson_complete_button("phase3", "lesson_3_3_gridsearchcv", 200, key="p3_l33")
    
    elif phase3_page == "Quiz":
        st.subheader("Phase 3 Quiz: Pipelines, ColumnTransformer, and GridSearchCV")
        
        try:
            with open('challenges/mcq/phase3_questions.json', 'r') as f:
                phase3_questions = json.load(f)
        except:
            st.error("Phase 3 quiz file not found. Please ensure challenges/mcq/phase3_questions.json exists.")
            phase3_questions = []
        
        if phase3_questions:
            for i, q in enumerate(phase3_questions):
                st.markdown(f"### Question {i+1}: {q['question']}")
                selected = st.radio(f"Choose answer (Q{i+1}):", q['options'], key=f"p3_q{i}")
                
                if st.button(f"Check (Q{i+1})", key=f"p3_check_q{i}"):
                    if selected == q['correct']:
                        st.success(f"✅ Correct! +{q.get('xp', 50)} XP")
                        save_quiz_result(f"phase3_q{i}", True, q.get('xp', 50))
                    else:
                        st.error(f"❌ Incorrect. Correct answer: {q['correct']}")
                        st.info(f"💡 {q['explanation']}")
                        save_quiz_result(f"phase3_q{i}", False, 0)
                st.divider()
        else:
            st.warning("No quiz questions available for Phase 3 yet.")
    
    elif phase3_page == "Code Challenges":
        st.subheader("Phase 3 Code Challenges")
        
        try:
            with open('challenges/code/phase3_challenges.json', 'r') as f:
                phase3_challenges = json.load(f)
        except:
            st.error("Phase 3 code challenges file not found.")
            phase3_challenges = []
        
        if phase3_challenges:
            challenge_select = st.selectbox(
                "Select a challenge:",
                [c['title'] for c in phase3_challenges],
                key="p3_challenge_select"
            )
            
            challenge = next((c for c in phase3_challenges if c['title'] == challenge_select), None)
            if challenge:
                st.markdown(f"**Difficulty:** {challenge['difficulty']}")
                st.markdown(challenge['description'])
                
                st.markdown("**Starter Code:**")
                st.code(challenge.get('starter_code', "# Write your solution here"), language='python')
                
                user_code = st.text_area("Your Solution:", height=200, key=f"p3_code_{challenge['id']}")
                
                if st.button("Run & Test", key=f"p3_run_{challenge['id']}"):
                    result = grade_code_challenge(user_code, challenge.get('solution', ''), challenge['id'])
                    if result['passed']:
                        st.success(f"✅ Challenge completed! +{challenge.get('xp', 100)} XP")
                        render_challenge_complete_button("phase3", challenge['id'], challenge.get('xp', 100), key=f"p3_complete_{challenge['id']}")
                    else:
                        st.error(f"❌ Tests failed: {result['error']}")
                        if challenge.get('hints'):
                            with st.expander("💡 Hint"):
                                st.markdown(challenge['hints'][0] if isinstance(challenge['hints'], list) else challenge['hints'])
        else:
            st.info("No code challenges available for Phase 3 yet.")

# ============================================
# PHASE 4: SUPERVISED LEARNING
# ============================================

elif phase_select == "🟫 Phase 4: Supervised Learning":
    st.title("🟫 Phase 4: Supervised Learning")
    st.info("🚀 Phase 4 covers Regression, Classification, and Ensemble Methods — the core supervised learning toolkit.")
    
    # Load Phase 4 quiz and challenges
    try:
        with open('challenges/mcq/phase4_questions.json', 'r', encoding='utf-8') as f:
            phase4_questions = json.load(f)
    except:
        phase4_questions = []

    try:
        with open('challenges/code/phase4_challenges.json', 'r', encoding='utf-8') as f:
            phase4_challenges = json.load(f)
    except:
        phase4_challenges = []
    
    phase4_page = st.sidebar.radio("Phase 4:", [
        "Overview",
        "Lesson 4.1",
        "Lesson 4.2",
        "Lesson 4.3",
        "Quiz",
        "Code Challenges"
    ])
    if phase4_page == "Overview":
        st.markdown("""
        ## Phase 4: Supervised Learning
        
        Master regression, classification, and ensemble methods for real-world predictive modeling.
        
        **What You'll Learn:**
        - **Regression:** Linear, polynomial, ridge/lasso regularization, evaluation metrics
        - **Classification:** Logistic regression, decision trees, SVMs, classification metrics
        - **Ensemble Methods:** Random forests, gradient boosting, voting classifiers
        
        **Key Skills:**
        - Build and train supervised learning models
        - Evaluate models with appropriate metrics
        - Handle imbalanced data
        - Tune hyperparameters systematically
        - Interpret model results
        
        **XP Available:** ~3,325 XP (3 lessons + 15 quiz + 10 challenges)
        """)
    
    elif phase4_page == "Lesson 4.1":
        st.header("📚 Lesson 4.1: Regression Models")
        tabs = st.tabs(["📖 Content", "💻 Examples", "🎯 Best Practices", "✅ Complete"])
        with tabs[0]:
            st.markdown("""
## Linear Regression
Linear regression models the relationship between features and a target using a linear function.

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
r2 = model.score(X_test, y_test)
```

**Key Metrics:** R², MAE, RMSE — each tells a different story about model quality.

---

## Ridge & Lasso Regularization
Ridge (L2) and Lasso (L1) add penalties to prevent overfitting by shrinking coefficients.

```python
from sklearn.linear_model import Ridge, Lasso
ridge = Ridge(alpha=1.0)  # L2: shrinks but rarely to zero
lasso = Lasso(alpha=0.1)  # L1: can shrink to exactly zero (feature selection)
```

---

## Polynomial Regression
Extend linear regression with polynomial features to capture non-linear relationships.

```python
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_train)
model = LinearRegression().fit(X_poly, y_train)
```

---

## Evaluation Metrics

| Metric | Formula | When to Use |
|--------|---------|-------------|
| **R²** | 1 - (SS_res / SS_tot) | Overall variance explained (0-1) |
| **MAE** | Mean(|y_true - y_pred|) | Average error (same units as y) |
| **RMSE** | √(Mean((y_true - y_pred)²)) | Penalizes large errors more |

---

**Best Practices:**
1. Always scale features before Ridge/Lasso
2. Use cross-validation to select hyperparameters
3. Check residual plots for model assumptions
4. Report multiple metrics, not just R²
            """)
        with tabs[1]:
            st.code("""# Example 1: Linear Regression
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
print(f"R²: {model.score(X_test, y_test):.4f}")

# Example 2: Ridge Regression
from sklearn.linear_model import Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_scaled, y_train)
print(f"Ridge R²: {ridge.score(X_test_scaled, y_test):.4f}")

# Example 3: GridSearchCV for alpha tuning
from sklearn.model_selection import GridSearchCV
param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10, 100]}
grid = GridSearchCV(Ridge(), param_grid, cv=5)
grid.fit(X_train_scaled, y_train)
print(f"Best alpha: {grid.best_params_['alpha']}")
            """, language='python')
        with tabs[2]:
            st.markdown("""
- **Scale features** for regularized models
- **Use cross-validation** for hyperparameter selection
- **Check assumptions:** Plot residuals, check normality
- **Interpret coefficients** carefully (depends on scaling)
- **Compare metrics:** R², MAE, RMSE together
            """)
        with tabs[3]:
            render_lesson_complete_button("phase4", "4.1", 200, key="p4_lesson1_complete")
    
    elif phase4_page == "Lesson 4.2":
        st.header("📚 Lesson 4.2: Classification Models")
        tabs = st.tabs(["📖 Content", "💻 Examples", "🎯 Best Practices", "✅ Complete"])
        with tabs[0]:
            st.markdown("""
## Logistic Regression
Despite its name, logistic regression predicts probabilities for classification.

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)  # Probabilities for each class
```

---

## Decision Trees
Tree-based models that recursively split features. Interpretable but can overfit.

```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)
importances = model.feature_importances_
```

---

## Support Vector Machines (SVM)
Find optimal hyperplane to separate classes with maximum margin.

```python
from sklearn.svm import SVC
svm = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
svm.fit(X_train_scaled, y_train)  # Always scale for SVM!
```

---

## Random Forests (Classification)
Ensemble of decision trees that reduces variance via bagging.

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(X_train, y_train)
```

---

## Classification Metrics

| Metric | When to Use |
|--------|-------------|
| **Accuracy** | Balanced classes only |
| **Precision** | Minimize false positives (spam) |
| **Recall** | Minimize false negatives (disease) |
| **F1-Score** | Balance precision and recall |
| **ROC AUC** | Imbalanced data, ranking models |

---

**Handling Imbalanced Data:**
```python
# Method 1: Class weights
model = RandomForestClassifier(class_weight='balanced')

# Method 2: Threshold optimization
y_pred = (y_proba >= 0.3).astype(int)  # Lower threshold for higher recall

# Method 3: SMOTE resampling
from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
```
            """)
        with tabs[1]:
            st.code("""# Example 1: Logistic Regression
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test):.4f}")

# Example 2: Decision Tree
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(max_depth=5)
tree.fit(X_train, y_train)
print(f"Tree Accuracy: {tree.score(X_test, y_test):.4f}")

# Example 3: Classification Report
from sklearn.metrics import classification_report
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Example 4: ROC AUC
from sklearn.metrics import roc_auc_score
y_proba = model.predict_proba(X_test)[:, 1]
print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")
            """, language='python')
        with tabs[2]:
            st.markdown("""
- **Choose metric carefully** — accuracy misleading on imbalanced data
- **Scale features** for SVM and regularized models
- **Control tree depth** to prevent overfitting
- **Cross-validate** to evaluate robustly
- **Report multiple metrics** — don't rely on accuracy alone
            """)
        with tabs[3]:
            render_lesson_complete_button("phase4", "4.2", 200, key="p4_lesson2_complete")
    
    elif phase4_page == "Lesson 4.3":
        st.header("📚 Lesson 4.3: Ensemble Methods & Evaluation")
        tabs = st.tabs(["📖 Content", "💻 Examples", "🎯 Best Practices", "✅ Complete"])
        with tabs[0]:
            st.markdown("""
## Voting Classifiers
Combine predictions from multiple models via hard or soft voting.

```python
from sklearn.ensemble import VotingClassifier
voting = VotingClassifier(
    estimators=[('lr', LogisticRegression()), ('rf', RandomForestClassifier())],
    voting='soft'  # Average probabilities, not just votes
)
voting.fit(X_train, y_train)
```

---

## Bagging & Random Forests
Train multiple models on random subsets of data, then average predictions.

```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
```

---

## Boosting: Gradient Boosting
Sequentially train models, each correcting errors of previous ones.

```python
from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
gbc.fit(X_train, y_train)
```

---

## Hyperparameter Tuning: GridSearchCV
Systematically search over parameter combinations.

```python
from sklearn.model_selection import GridSearchCV
params = {'n_estimators': [50, 100], 'max_depth': [3, 5, 7]}
grid = GridSearchCV(GradientBoostingClassifier(), params, cv=5)
grid.fit(X_train, y_train)
print(f"Best params: {grid.best_params_}")
print(f"Best CV score: {grid.best_score_:.4f}")
```

---

## Advanced: Cross-Validation for Evaluation

```python
from sklearn.model_selection import cross_validate, StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True)
scoring = {'accuracy': 'accuracy', 'f1': 'f1', 'roc_auc': 'roc_auc'}
results = cross_validate(model, X, y, cv=cv, scoring=scoring)
# Report mean and std of each metric
```

---

**Key Principles:**
1. **Ensemble diversity** — use different model types
2. **Data leakage prevention** — include preprocessing in pipeline
3. **Robust evaluation** — use cross-validation, report CI
4. **Systematic tuning** — GridSearchCV or RandomizedSearchCV
5. **Business metrics** — choose metrics aligned with goals
            """)
        with tabs[1]:
            st.code("""# Example 1: Voting Classifier
from sklearn.ensemble import VotingClassifier
voting = VotingClassifier(
    estimators=[('lr', LogisticRegression()), 
                ('rf', RandomForestClassifier()), 
                ('svm', SVC(probability=True))],
    voting='soft'
)
voting.fit(X_train, y_train)
print(f"Ensemble: {voting.score(X_test, y_test):.4f}")

# Example 2: Gradient Boosting
from sklearn.ensemble import GradientBoostingClassifier
gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1)
gbc.fit(X_train, y_train)
print(f"GBC: {gbc.score(X_test, y_test):.4f}")

# Example 3: GridSearchCV
from sklearn.model_selection import GridSearchCV
params = {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1]}
grid = GridSearchCV(GradientBoostingClassifier(), params, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)
print(f"Best: {grid.best_params_}, Score: {grid.best_score_:.4f}")
            """, language='python')
        with tabs[2]:
            st.markdown("""
- **Start simple** before using ensembles
- **Ensure model diversity** in ensemble
- **Use soft voting** (average probabilities)
- **Tune learning rate** carefully in boosting
- **Monitor overfitting:** CV score vs test score
- **Save best model** with joblib for production
            """)
        with tabs[3]:
            render_lesson_complete_button("phase4", "4.3", 200, key="p4_lesson3_complete")
    
    elif phase4_page == "Quiz":
        st.header("❓ Phase 4 Quiz")
        if phase4_questions:
            for idx, q in enumerate(phase4_questions, 1):
                st.markdown(f"### Q{idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p4_q{q['id']}")
                if st.button("Submit", key=f"p4_submit_{q['id']}"):
                    correct = selected == q["options"][q["correct"]]
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        save_quiz("phase4", q['id'], selected, True, q['xp'])
                    else:
                        st.error("❌ Incorrect")
                    st.info(q["explanation"])
                st.markdown("---")
        else:
            st.info("Loading Phase 4 quiz questions...")
    
    elif phase4_page == "Code Challenges":
        st.header("💻 Phase 4 Code Challenges")
        if phase4_challenges:
            for challenge in phase4_challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p4_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase4", challenge['id'], challenge.get('xp', 100), key=f"p4_complete_{challenge['id']}")
        else:
            st.info("Loading Phase 4 code challenges...")

# ============================================
# PHASE 5: UNSUPERVISED LEARNING
# ============================================

elif phase_select == "🟧 Phase 5: Unsupervised & Representation":
    st.title("🟧 Phase 5: Unsupervised & Representation")
    
    # Load Phase 5 quiz and challenges
    try:
        with open('challenges/mcq/phase5_questions.json', 'r', encoding='utf-8') as f:
            phase5_questions = json.load(f)
    except:
        phase5_questions = []

    try:
        with open('challenges/code/phase5_challenges.json', 'r', encoding='utf-8') as f:
            phase5_challenges = json.load(f)
    except:
        phase5_challenges = []
    
    phase5_page = st.sidebar.radio("Phase 5:", [
        "Overview",
        "Lesson 5.1",
        "Lesson 5.2",
        "Lesson 5.3",
        "Quiz",
        "Code Challenges"
    ])
    if phase5_page == "Overview":
        st.markdown("""
        ## Phase 5: Unsupervised & Representation

        Learn how to discover structure in unlabeled data and transform complex feature spaces.

        **Topics:**
        - Clustering with KMeans, DBSCAN, and hierarchical methods
        - Dimensionality reduction with PCA and visualization techniques
        - Anomaly detection and unsupervised model validation
        """)
    elif phase5_page == "Lesson 5.1":
        st.header("📚 Lesson 5.1: K-Means Clustering & DBSCAN")
        st.markdown("""
## K-Means Clustering
KMeans partitions data into K clusters by minimizing intra-cluster variance.

### When to use it
- Data has roughly spherical clusters
- You can estimate the number of clusters
- Speed matters for medium-sized datasets

### Example
```python
from sklearn.cluster import KMeans
import numpy as np

X = np.random.randn(100, 2)
model = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = model.fit_predict(X)
print(model.cluster_centers_)
```

### Choosing K
Use the elbow method, silhouette score, or domain knowledge to choose the right number of clusters.

### DBSCAN for density-based clusters
DBSCAN groups points by density and identifies noise automatically.

```python
from sklearn.cluster import DBSCAN
model = DBSCAN(eps=0.5, min_samples=5)
labels = model.fit_predict(X)
```

### Strengths and limitations
- ✅ Handles arbitrary-shaped clusters
- ✅ Detects noise/outliers
- ❌ Sensitive to eps/min_samples
- ❌ Struggles with varying density
        """)
        st.code("""from sklearn.cluster import KMeans, DBSCAN
import numpy as np

X = np.random.randn(200, 2)

kmeans = KMeans(n_clusters=4, random_state=42)
kmeans_labels = kmeans.fit_predict(X)

dbscan = DBSCAN(eps=0.4, min_samples=5)
dbscan_labels = dbscan.fit_predict(X)

print('KMeans cluster labels:', set(kmeans_labels))
print('DBSCAN cluster labels:', set(dbscan_labels))
""", language='python')
        render_lesson_complete_button("phase5", "5.1", 100, key="p5_lesson1_complete")
    elif phase5_page == "Lesson 5.2":
        st.header("📚 Lesson 5.2: PCA & Dimensionality Reduction")
        st.markdown("""
## Principal Component Analysis (PCA)
PCA reduces dimensionality by projecting data onto principal components that capture the most variance.

### Why it matters
- Faster training
- Better visualization
- Less noise and overfitting
- Better generalization for high-dimensional data

### Workflow
1. Standardize features
2. Compute principal components
3. Project data onto top components

### Example
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)
```

### PCA vs t-SNE/UMAP
| Method | Purpose | Best for |
|--------|---------|----------|
| PCA | Linear reduction | Preprocessing and compression |
| t-SNE | Visualization | 2D/3D cluster inspection |
| UMAP | Visualization | Large datasets and structure exploration |

### Practical note
Use PCA for preprocessing and feature compression, and use t-SNE/UMAP for exploratory visualization.
        """)
        st.code("""from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=3)
X_reduced = pca.fit_transform(X_scaled)
print('Explained variance:', pca.explained_variance_ratio_)
""", language='python')
        render_lesson_complete_button("phase5", "5.2", 100, key="p5_lesson2_complete")
    elif phase5_page == "Lesson 5.3":
        st.header("📚 Lesson 5.3: Hierarchical Clustering, Manifolds & Anomaly Detection")
        st.markdown("""
## Hierarchical Clustering
Agglomerative clustering builds nested clusters by merging points iteratively.

### Use when
- You want a dendrogram
- The dataset is small or medium-sized
- You want flexible cluster counts after fitting

### Example
```python
from sklearn.cluster import AgglomerativeClustering
model = AgglomerativeClustering(n_clusters=4)
labels = model.fit_predict(X)
```

## Manifold Learning
Non-linear dimensionality reduction methods like t-SNE and UMAP help visualize complex structure.

### Example with t-SNE
```python
from sklearn.manifold import TSNE
X_embedded = TSNE(n_components=2, random_state=42).fit_transform(X_scaled)
```

### Example with UMAP
```python
import umap
X_umap = umap.UMAP(n_components=2, random_state=42).fit_transform(X_scaled)
```

## Anomaly Detection
Anomaly detection finds unusual points that differ from normal patterns.

### Isolation Forest
```python
from sklearn.ensemble import IsolationForest
model = IsolationForest(contamination=0.1, random_state=42)
labels = model.fit_predict(X)
```

### Local Outlier Factor
```python
from sklearn.neighbors import LocalOutlierFactor
model = LocalOutlierFactor(n_neighbors=20)
labels = model.fit_predict(X)
```

### Key techniques
- `IsolationForest` — tree-based anomaly scoring
- `LocalOutlierFactor` — density-based detection
- `OneClassSVM` — boundary-based anomaly detection
- `t-SNE` / `UMAP` — visualize clusters and anomalies in 2D
        """)
        st.code("""from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

iso = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
iso_preds = iso.fit_predict(X)

lof = LocalOutlierFactor(n_neighbors=20)
lof_preds = lof.fit_predict(X)

print('IsolationForest anomalies:', (iso_preds == -1).sum())
print('LOF anomalies:', (lof_preds == -1).sum())
""", language='python')
        render_lesson_complete_button("phase5", "5.3", 100, key="p5_lesson3_complete")
    elif phase5_page == "Quiz":
        st.header("❓ Phase 5 Quiz")
        if phase5_questions:
            for idx, q in enumerate(phase5_questions, 1):
                st.markdown(f"### Q{idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p5_q{q['id']}")
                if st.button("Submit", key=f"p5_submit_{q['id']}"):
                    correct = selected == q["options"][q["correct"]]
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        save_quiz("phase5", q['id'], selected, True, q['xp'])
                    else:
                        st.error("❌ Incorrect")
                    st.info(q["explanation"])
                st.markdown("---")
        else:
            st.info("No Phase 5 quiz questions found yet.")
    elif phase5_page == "Code Challenges":
        st.header("💻 Phase 5 Code Challenges")
        if phase5_challenges:
            for challenge in phase5_challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p5_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase5", challenge['id'], challenge.get('xp', 100), key=f"p5_complete_{challenge['id']}")
        else:
            st.info("No Phase 5 challenges found yet.")

# ============================================
# PHASE 5: MODEL EVALUATION
# ============================================

    # Load Phase 6 quiz and challenges
    try:
        with open('challenges/mcq/phase6_questions.json', 'r', encoding='utf-8') as f:
            phase6_questions = json.load(f)
    except:
        phase6_questions = []

    try:
        with open('challenges/code/phase6_challenges.json', 'r', encoding='utf-8') as f:
            phase6_challenges = json.load(f)
    except:
        phase6_challenges = []

elif phase_select == "🟨 Phase 6: Model Evaluation & Robustness":
    st.title("🟨 Phase 6: Model Evaluation & Robustness")
    phase6_page = st.sidebar.radio("Phase 6:", [
        "Overview",
        "Lesson 6.1",
        "Lesson 6.2",
        "Lesson 6.3",
        "Quiz",
        "Code Challenges"
    ])
    if phase6_page == "Overview":
        st.markdown("""
        ## Phase 6: Model Evaluation & Robustness

        Master metrics, validation strategies, and techniques for evaluating ML models correctly.

        **Topics:**
        - Classification metrics (precision, recall, F1, ROC AUC)
        - Cross-validation and stratification
        - Feature selection and importance
        - Model calibration and learning curves
        - Handling imbalanced data (class weights, SMOTE)
        - Threshold tuning for business objectives
        """)
    elif phase6_page == "Lesson 6.1":
        st.header("📚 Lesson 6.1: Classification Metrics")
        st.markdown("""
## Why Accuracy Isn't Enough

With **imbalanced datasets**, accuracy is misleading. A model predicting "No disease" always gets 95% accuracy if only 5% have disease - but it's useless!

## Key Metrics

### 1. Precision: "Of positives we predict, how many are correct?"
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

**Use when**: False positives are costly (spam filter, disease screening)

### 2. Recall (Sensitivity): "Of actual positives, how many did we find?"
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

**Use when**: False negatives are costly (cancer detection, fraud)

### 3. F1 Score: Harmonic mean of precision and recall
$$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

**Use when**: You want balance, especially with imbalanced data

### 4. ROC AUC: Measures ability to distinguish classes at all thresholds
- **AUC = 0.5**: Random classifier
- **AUC = 1.0**: Perfect classifier
- **AUC = 0.7-0.8**: Good classifier

**Use when**: Comparing models, need threshold-independent evaluation

## Confusion Matrix Breakdown

```
                    Predicted Positive    Predicted Negative
Actual Positive              TP                   FN
Actual Negative              FP                   TN
```

## Implementation

```python
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import confusion_matrix, classification_report

# Binary classification
y_true = [0, 0, 1, 1, 1, 0, 1, 0]
y_pred = [0, 0, 1, 0, 1, 0, 1, 1]
y_proba = [0.1, 0.2, 0.9, 0.3, 0.8, 0.2, 0.85, 0.6]

# Individual metrics
print(f"Precision: {precision_score(y_true, y_pred):.3f}")
print(f"Recall: {recall_score(y_true, y_pred):.3f}")
print(f"F1 Score: {f1_score(y_true, y_pred):.3f}")
print(f"ROC AUC: {roc_auc_score(y_true, y_proba):.3f}")

# All at once
print(classification_report(y_true, y_pred))

# Confusion matrix
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(f"TP={tp}, TN={tn}, FP={fp}, FN={fn}")
```

## Precision vs Recall Tradeoff

**Higher Precision** = Trust predictions, but miss some positives
**Higher Recall** = Catch all positives, but with false alarms

Choose based on cost of errors:
- **Medical diagnosis**: Prioritize Recall (don't miss diseases)
- **Spam filter**: Prioritize Precision (don't flag legitimate emails)
- **Fraud detection**: Often use F1 (balanced approach)
        """)
        render_lesson_complete_button("phase6", "6.1", 200, key="p6_lesson1_complete")
    elif phase6_page == "Lesson 6.2":
        st.header("📚 Lesson 6.2: Cross-Validation & Feature Selection")
        st.markdown("""
## Why K-Fold Cross-Validation?

Single train/test split may be lucky or unlucky. K-fold uses multiple splits:

**K-Fold Process:**
1. Split data into K equal folds
2. For each fold: train on K-1 folds, test on 1 fold
3. Average K scores for robust estimate

## Implementation

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

# Regular K-Fold
scores = cross_val_score(model, X, y, cv=5, scoring='f1')
print(f"F1 scores: {scores}")
print(f"Mean: {scores.mean():.3f} (+/- {scores.std():.3f})")

# Stratified K-Fold for imbalanced data
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='f1')
```

**Stratified K-Fold ensures** each fold has same class distribution as original data.

## Feature Selection

**Goal**: Remove irrelevant/redundant features
- Simpler models
- Faster training
- Better generalization
- Easier interpretation

### Methods

**1. Permutation Importance (Model-Agnostic)**
```python
from sklearn.inspection import permutation_importance

perm_imp = permutation_importance(model, X_test, y_test, n_repeats=10)
# Works with any model type
```

**2. Recursive Feature Elimination (RFE)**
```python
from sklearn.feature_selection import RFE

rfe = RFE(model, n_features_to_select=10)
rfe.fit(X_train, y_train)
selected_features = X.columns[rfe.support_]
```

Trains model → removes least important → repeats. Captures interactions.

**3. Built-in Feature Importance**
```python
# Tree-based models only
importances = model.feature_importances_
```

### Complete Example

```python
from sklearn.datasets import load_breast_cancer
from sklearn.inspection import permutation_importance
import pandas as pd

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

model.fit(X_train, y_train)

# Get importance
perm_imp = permutation_importance(model, X_test, y_test)
imp_df = pd.DataFrame({
    'feature': X.columns,
    'importance': perm_imp.importances_mean
}).sort_values('importance', ascending=False)

print(imp_df.head(10))  # Top 10 features
```

## When to Use Feature Selection

✅ **Many features** (1000+) → Select top features
✅ **Correlated features** → Remove redundant ones
✅ **Interpretability** → Fewer features = easier explanation
✅ **Training speed** → Fewer features = faster model
        """)
        render_lesson_complete_button("phase6", "6.2", 200, key="p6_lesson2_complete")
    elif phase6_page == "Lesson 6.3":
        st.header("📚 Lesson 6.3: Model Calibration & Learning Curves")
        st.markdown("""
## Model Calibration

**Definition**: Predicted probabilities match true probabilities

**Calibrated Model**: If model predicts 0.7 probability → ~70% actually positive

**Why It Matters**: For probability-based decisions (medical diagnosis, fraud scoring)

## Calibration Methods

**1. Isotonic Regression** (flexible, needs more data)
**2. Sigmoid (Platt Scaling)** (simple, works well for logistic regression)

```python
from sklearn.calibration import CalibratedClassifierCV

# Apply calibration
calibrated_model = CalibratedClassifierCV(model, method='sigmoid', cv=5)
calibrated_model.fit(X_train, y_train)
y_proba_cal = calibrated_model.predict_proba(X_test)[:, 1]
```

## Learning Curves

**Purpose**: Diagnose **bias vs variance** (underfitting vs overfitting)

**How**: Plot train/validation error vs training set size

**Patterns:**
- **Large gap** = Overfitting (high variance)
- **Both high** = Underfitting (high bias)
- **Curves converge** = Good fit

```python
from sklearn.model_selection import learning_curve
import numpy as np

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5, 
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy'
)

# Plot with confidence bands
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
val_mean = np.mean(val_scores, axis=1)
val_std = np.std(val_scores, axis=1)

plt.plot(train_sizes, train_mean, label='Train')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.2)
plt.plot(train_sizes, val_mean, label='Validation')
plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.2)
plt.legend()
plt.show()
```

## Handling Imbalanced Data

**Multi-pronged approach:**

1. **Class Weights**: Penalize minority class misclassification
   ```python
   model = LogisticRegression(class_weight='balanced')
   ```

2. **Stratified Cross-Validation**: Preserve class distribution
   ```python
   skf = StratifiedKFold(n_splits=5, shuffle=True)
   ```

3. **SMOTE**: Generate synthetic minority samples
   ```python
   from imblearn.over_sampling import SMOTE
   X_resampled, y_resampled = SMOTE().fit_resample(X_train, y_train)
   ```

4. **Appropriate Metrics**: Use F1, ROC AUC (not accuracy)

5. **Threshold Tuning**: Adjust decision boundary
   ```python
   # Lower threshold = higher recall, more false positives
   y_pred = (y_proba >= 0.3).astype(int)
   ```

## Choosing Threshold

Default is 0.5, but adjust based on business cost:
- **Medical**: Lower threshold (catch disease)
- **Fraud**: Lower threshold (catch fraud)
- **Spam**: Higher threshold (avoid false positives)

```python
from sklearn.metrics import precision_recall_curve

precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * (precision[:-1] * recall[:-1]) / (precision[:-1] + recall[:-1] + 1e-10)
best_threshold = thresholds[np.argmax(f1_scores)]
```

## Complete Evaluation Pipeline

```python
# 1. Stratified CV for robust estimate
from sklearn.model_selection import StratifiedKFold, cross_validate

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_validate(
    model, X, y, cv=skf,
    scoring=['precision', 'recall', 'f1', 'roc_auc']
)

# 2. Check calibration
from sklearn.calibration import calibration_curve
prob_true, prob_pred = calibration_curve(y_test, y_proba, n_bins=10)

# 3. Plot learning curve
train_sizes, train_scores, val_scores = learning_curve(model, X, y, cv=5)

# 4. Tune threshold if needed
y_pred_tuned = (y_proba >= best_threshold).astype(int)
```
        """)
        render_lesson_complete_button("phase6", "6.3", 200, key="p6_lesson3_complete")
    elif phase6_page == "Quiz":
        st.header("❓ Phase 6 Quiz")
        if phase6_questions:
            for idx, q in enumerate(phase6_questions, 1):
                st.markdown(f"### Q{idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p6_q{q['id']}")
                if st.button("Submit", key=f"p6_submit_{q['id']}"):
                    correct = selected == q["options"][q["correct"]]
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        save_quiz("phase6", q['id'], selected, True, q['xp'])
                    else:
                        st.error("❌ Incorrect")
                    st.info(q["explanation"])
                st.markdown("---")
        else:
            st.info("No Phase 6 quiz questions found yet.")
    elif phase6_page == "Code Challenges":
        st.header("💻 Phase 6 Code Challenges")
        if phase6_challenges:
            for challenge in phase6_challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p6_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase6", challenge['id'], challenge.get('xp', 125), key=f"p6_complete_{challenge['id']}")
        else:
            st.info("No Phase 6 challenges found yet.")


# ============================================
# PHASE 6: ADVANCED ML
# ============================================

elif phase_select == "🔴 Phase 6: Advanced ML (Legacy)":
    phase6_page = st.sidebar.radio("Phase 6 Legacy:", [
        "Overview",
        "Lesson 6.1",
        "Lesson 6.2",
        "Lesson 6.3",
        "Quiz",
        "Code Challenges"
    ])

    if phase6_page == "Overview":
        st.header("🟥 Phase 6: Advanced ML")
        st.markdown("""
## Advanced Machine Learning

Learn advanced techniques for production-ready ML models.

**Topics:**
- Feature engineering and scaling
- Hyperparameter tuning with GridSearch
- Handling imbalanced data
- Detecting overfitting and underfitting
- Learning curves and model diagnostics
        """)
    elif phase6_page == "Lesson 6.1":
        st.header("📚 Lesson 6.1: Feature Engineering & Scaling")
        st.markdown("""
## Feature Engineering

Feature engineering is the process of selecting, transforming, and creating features to improve model performance.

### Why Feature Engineering Matters

🎯 **Better data → Better models**
- Raw data rarely performs optimally
- Features can amplify or reduce signal
- Engineering often outweighs algorithm choice

### Common Techniques

**1. Scaling/Normalization**

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# StandardScaler: zero mean, unit variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# MinMaxScaler: [0, 1] range
minmax = MinMaxScaler()
X_minmax = minmax.fit_transform(X)
```

**When to use:**
- ✅ KNN, SVM, Neural Networks (distance-based)
- ✅ Linear/Logistic Regression (gradient descent)
- ❌ Tree-based models (scale-invariant)

**2. Encoding Categorical Variables**

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Label Encoding: ordinal categories (0, 1, 2...)
le = LabelEncoder()
X['color'] = le.fit_transform(['red', 'blue', 'red', 'green'])

# One-Hot Encoding: dummy variables
X = pd.get_dummies(X, columns=['color'], drop_first=True)
```

**3. Polynomial Features**

```python
from sklearn.preprocessing import PolynomialFeatures

# Create interactions and polynomial terms
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)  # Adds X², X*Y, etc.
```

**4. Feature Selection**

```python
from sklearn.feature_selection import SelectKBest, f_classif

# Keep top K features
selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)
```

### Feature Scaling Best Practices

⚠️ **Always fit scaler on training data only**

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # fit AND transform
X_test_scaled = scaler.transform(X_test)        # transform only!
```

Fitting on test data = **DATA LEAKAGE**
        """)
        render_lesson_complete_button("phase6", "6.1", 100, key="p6_lesson1_complete")
    elif phase6_page == "Lesson 6.2":
        st.header("📚 Lesson 6.2: Hyperparameter Tuning")
        st.markdown("""
## What are Hyperparameters?

**Parameters**: Learned during training (weights, biases)

**Hyperparameters**: Set before training, control learning process
- Learning rate, number of trees, max depth, regularization strength

## GridSearchCV: Exhaustive Search

Test all combinations of hyperparameters and find the best.

### Implementation

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5],
    'max_features': ['sqrt', 'log2']
}

# GridSearchCV
model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    model, 
    param_grid,
    cv=5,                    # 5-fold cross-validation
    scoring='f1',            # optimization metric
    n_jobs=-1                # use all cores
)

grid_search.fit(X_train, y_train)

# Results
print(f"Best params: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.4f}")
print(f"Test score: {grid_search.score(X_test, y_test):.4f}")

# Use best model
best_model = grid_search.best_estimator_
```

## RandomizedSearchCV: Random Sampling

For large parameter spaces, randomly sample instead of testing all.

```python
from sklearn.model_selection import RandomizedSearchCV

random_search = RandomizedSearchCV(
    model,
    param_distributions=param_grid,
    n_iter=10,  # Test 10 random combinations
    cv=5
)
```

### Tips

🎯 **Start broad, then narrow**
- First pass: large parameter ranges
- Second pass: zoom in around best values

🎯 **Use meaningful ranges**
- n_estimators: [10, 500]
- max_depth: [3, 30]

🎯 **Consider computation time**
- Larger grids = longer training
- Use n_jobs=-1 for parallel processing
        """)
        render_lesson_complete_button("phase6", "6.2", 100, key="p6_lesson2_complete")
    elif phase6_page == "Lesson 6.3":
        st.header("📚 Lesson 6.3: Overfitting, Underfitting & Learning Curves")
        st.markdown("""
## Model Complexity Spectrum

```
UNDERFITTING          OPTIMAL          OVERFITTING
(High Bias)         (Sweet Spot)      (High Variance)

Low train acc    High train acc    Very high train acc
Low test acc     High test acc     LOW test acc
```

## Detecting Underfitting vs Overfitting

### Signs of Underfitting
- ❌ Low training accuracy
- ❌ Low test accuracy
- ❌ Model is too simple

**Solutions:**
1. Increase model complexity
2. Train longer
3. Better features

### Signs of Overfitting
- ✅ High training accuracy
- ❌ Low test accuracy
- ❌ Large gap between train/test

**Solutions:**
1. More training data
2. Reduce model complexity
3. Regularization (L1/L2)
4. Early stopping
5. Dropout (for neural networks)

## Learning Curves

Visualize training and validation scores vs dataset size.

```python
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy'
)

train_mean = np.mean(train_scores, axis=1)
val_mean = np.mean(val_scores, axis=1)

plt.plot(train_sizes, train_mean, label='Training')
plt.plot(train_sizes, val_mean, label='Validation')
plt.xlabel('Training Set Size')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
```

### Interpreting Learning Curves

**Underfitting**: Both curves low and converge
→ **Add more data won't help, increase complexity**

**Overfitting**: Gap between curves, training high
→ **Add more data or reduce complexity**

**Good Model**: Both curves high and close together
→ **Model is well-tuned**

## Handling Imbalanced Data

### Problem
If 95% of data is class 0 and 5% is class 1:
- Predicting always 0 gives 95% accuracy
- But misses all positive cases!

### Solutions

**1. SMOTE (Synthetic Minority Oversampling)**

```python
from imblearn.over_sampling import SMOTE

# ONLY on training data!
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
```

**2. Class Weights**

```python
model = RandomForestClassifier(
    class_weight='balanced',  # Penalize minority class less
    random_state=42
)
```

**3. Different Metrics**

Use F1, Precision, Recall, or AUC-ROC instead of accuracy.
        """)
    elif phase6_page == "Quiz":
        st.header("❓ Phase 6 Quiz")
        if phase6_questions:
            for idx, q in enumerate(phase6_questions, 1):
                st.markdown(f"### Q{idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p6_q{q['id']}")
                if st.button("Submit", key=f"p6_submit_{q['id']}"):
                    correct = selected == q["options"][q["correct"]]
                    if correct:
                        st.success(f"✅ Correct! {q.get('explanation', '')}")
                        save_quiz("phase6", q['id'], selected, True, 10)
                    else:
                        st.error(f"❌ Incorrect. {q.get('explanation', '')}")
                st.markdown("---")
        else:
            st.info("No Phase 6 quiz questions found yet.")
    elif phase6_page == "Code Challenges":
        st.header("💻 Phase 6 Code Challenges")
        if phase6_challenges:
            for challenge in phase6_challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p6_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase6", challenge['id'], challenge.get('xp', 100), key=f"p6_complete_{challenge['id']}")
        else:
            st.info("No Phase 6 challenges found yet.")

        st.markdown("---")
        st.subheader("🧪 Auto-Graded Challenge")
        task = CODE_GRADE_CHALLENGES["roc_auc_evaluator"]
        st.markdown(f"**{task['title']}** — Target ROC AUC: {task['target']:.2f}")
        user_code = st.text_area("Submit your code for grading:", value=task["starter_code"], height=260, key="p6_auto_code")
        if st.button("Run Auto-Grader", key="p6_run_autograder"):
            passed, message = grade_code_challenge("roc_auc_evaluator", user_code)
            if passed:
                if not is_challenge_complete(task["phase"], task["challenge_id"]):
                    save_progress(task["phase"], task["challenge_id"], "completed", task["xp"], "challenge")
                    st.success(f"✅ Passed! {message} You earned {task['xp']} XP.")
                else:
                    st.success(f"✅ Passed! {message} Challenge already completed.")
            else:
                st.error(f"❌ {message}")

# ============================================
# PHASE 7: PRODUCTION & MLOPS
# ============================================

elif phase_select == "🟦 Phase 7: Production & MLOps":
    st.title("🟦 Phase 7: Production & MLOps")

    # Use preloaded Phase 7 quiz and code challenge content
    phase7_questions = phase7_data['questions']
    phase7_challenges = phase7_data['code']

    phase7_page = st.sidebar.radio("Phase 7:", [
        "Overview",
        "Lesson 7.1",
        "Lesson 7.2",
        "Lesson 7.3",
        "Quiz",
        "Code Challenges"
    ])
    if phase7_page == "Overview":
        st.markdown("""
        ## Phase 7: Production & MLOps

        **Topics:**
        - Model persistence (`joblib` / `pickle`)
        - Serving with FastAPI / Streamlit
        - Containerization and deployment
        - Experiment tracking and monitoring
        - CI/CD, rollback, and model governance
        """)
    elif phase7_page == "Lesson 7.1":
        st.header("📚 Lesson 7.1: Model Persistence & Serving")
        st.markdown("""
## Model Persistence

Save trained models reliably for production use.

### Joblib vs Pickle
- `joblib.dump(model, 'model.joblib')`
- `joblib.load('model.joblib')`

**Best for**: storing scikit-learn models and transformers.

```python
import joblib
joblib.dump(model, 'model.joblib')
loaded_model = joblib.load('model.joblib')
```

## Serving Models

### FastAPI
Use FastAPI to build lightweight model APIs.

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load('model.joblib')

class InputData(BaseModel):
    feature1: float
    feature2: float

@app.post('/predict')
def predict(data: InputData):
    features = [[data.feature1, data.feature2]]
    prediction = model.predict(features)[0]
    return {'prediction': int(prediction)}
```

### Streamlit as a model UI
Streamlit can serve simple interactive demos and dashboards.

```python
import streamlit as st
model = joblib.load('model.joblib')
input_value = st.number_input('Feature 1')
pred = model.predict([[input_value, 2.0]])
st.write(pred)
```

### Best Practices
- Store preprocessing pipeline with model
- Avoid training and serving environments mismatch
- Keep API stateless and lightweight
        """)
        render_lesson_complete_button("phase7", "7.1", 200, key="p7_lesson1_complete")
    elif phase7_page == "Lesson 7.2":
        st.header("📚 Lesson 7.2: Containerization & Deployment")
        st.markdown("""
## Docker for ML

### Dockerfile example

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Why containerize?
- Repeatable environment
- Easier deployment
- Isolation of dependencies

## Kubernetes Basics

### Deployment
A Deployment manages replicas and rollout strategy.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: ml-model
        image: your-image
        ports:
        - containerPort: 8000
```

### Service
Expose the model service inside the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

### Best Practices
- Use health checks
- Separate config from code
- Use tags for versioned images
        """)
        render_lesson_complete_button("phase7", "7.2", 200, key="p7_lesson2_complete")
    elif phase7_page == "Lesson 7.3":
        st.header("📚 Lesson 7.3: Monitoring, Drift, and CI/CD")
        st.markdown("""
## Monitoring in Production

Track model performance and data quality.

### Data Drift
When input distribution changes over time, model predictions may degrade.

### Example drift metric
```python
import numpy as np
baseline_mean = np.mean(baseline_data)
new_mean = np.mean(new_data)
drift_score = abs(new_mean - baseline_mean)
```

## Model Rollback
If a deployment fails health checks or performance drops, rollback to a previous version.

## Experiment Tracking
Use MLflow to log parameters, metrics, and artifacts.

```python
import mlflow
mlflow.start_run()
mlflow.log_param('model', 'LogisticRegression')
mlflow.log_metric('accuracy', accuracy)
mlflow.sklearn.log_model(model, 'model')
mlflow.end_run()
```

## CI/CD Checklist
- Automated tests
- Container build and scan
- Deployment verification
- Monitoring and alerting
        """)
        render_lesson_complete_button("phase7", "7.3", 200, key="p7_lesson3_complete")
    elif phase7_page == "Quiz":
        st.header("❓ Phase 7 Quiz")
        if phase7_questions:
            for idx, q in enumerate(phase7_questions, 1):
                st.markdown(f"### Q{idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p7_q{q['id']}")
                if st.button("Submit", key=f"p7_submit_{q['id']}"):
                    correct = selected == q["options"][q["correct"]]
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        save_quiz("phase7", q['id'], selected, True, q['xp'])
                    else:
                        st.error("❌ Incorrect")
                    st.info(q["explanation"])
                st.markdown("---")
        else:
            st.info("No Phase 7 quiz questions found yet.")
    elif phase7_page == "Code Challenges":
        st.header("💻 Phase 7 Code Challenges")
        if phase7_challenges:
            for challenge in phase7_challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p7_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase7", challenge['id'], challenge.get('xp', 100), key=f"p7_complete_{challenge['id']}")
        else:
            st.info("No Phase 7 challenges found yet.")

elif phase_select == "🟫 Phase 8: Advanced / Edge Topics":
    st.title("🟫 Phase 8: Advanced / Edge Topics")
    phase8_page = st.sidebar.radio("Phase 8:", [
        "Overview",
        "Lesson 8.1",
        "Lesson 8.2",
        "Lesson 8.3",
        "Quiz",
        "Code Challenges"
    ])
    if phase8_page == "Overview":
        st.markdown("""
        ## Phase 8: Advanced / Edge Topics

        This phase covers advanced patterns and edge-case ML workflows.

        **Topics include:**
        - Incremental learning and `partial_fit`
        - Explainability with permutation importance and model inspection
        - Custom estimator design and compatibility with pipelines
        - Time-series and streaming pipeline patterns for memory-constrained data
        """)
    elif phase8_page == "Lesson 8.1":
        st.header("📚 Lesson 8.1: Incremental Learning")
        st.markdown("""
## Incremental Learning
Some scikit-learn estimators support `partial_fit()` for batch-by-batch training, which is useful for streaming data and datasets that do not fit in memory.

### Partial fit workflow
- Train on a batch
- Update the model incrementally
- Repeat for the next batch

### Important detail
The first `partial_fit()` call usually requires the full list of target classes:
```python
clf.partial_fit(X_batch, y_batch, classes=classes)
```

### Compatible estimators
- `SGDClassifier`, `SGDRegressor`
- `PassiveAggressiveClassifier`
- `MiniBatchKMeans`
- `HashingVectorizer` + linear models for text pipelines

### Example with SGDClassifier
```python
from sklearn.linear_model import SGDClassifier

clf = SGDClassifier(max_iter=1000, tol=1e-3)
for X_batch, y_batch in batches:
    clf.partial_fit(X_batch, y_batch, classes=classes)
```

### When to use it
- Very large datasets
- Streaming or incremental data
- Memory-constrained environments

### Related techniques
- `MiniBatchKMeans` for scalable clustering
- `warm_start=True` for iterative estimators
- out-of-core preprocessing with `partial_fit`
""")
        st.code("""from sklearn.linear_model import SGDClassifier
from sklearn.cluster import MiniBatchKMeans

clf = SGDClassifier(max_iter=1000, tol=1e-3)
for X_batch, y_batch in batches:
    clf.partial_fit(X_batch, y_batch, classes=classes)

mbk = MiniBatchKMeans(n_clusters=4, batch_size=32, random_state=42)
mbk.partial_fit(X_batch)
""", language='python')
        render_lesson_complete_button("phase8", "8.1", 200, key="p8_lesson1_complete")
    elif phase8_page == "Lesson 8.2":
        st.header("📚 Lesson 8.2: Explainability & Feature Importance")
        st.markdown("""
## Explainability
Explainability helps you understand model behavior and feature impact.

### Permutation importance
Permutation importance measures the change in score when a feature is randomly shuffled.

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
print(result.importances_mean)
```

### Feature importance sources
- `feature_importances_` for tree-based models
- coefficients for linear models
- permutation importance for any fitted estimator
- SHAP and partial dependence for richer model explanations

### Practical guidance
- Compare importance across models
- Use explainability to detect drift and debug models
- Use importance scores to prioritize feature engineering
- Compare multiple explainability techniques for production
""")
        st.code("""from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
for name, score in zip(feature_names, result.importances_mean):
    print(name, score)
""", language='python')
        render_lesson_complete_button("phase8", "8.2", 200, key="p8_lesson2_complete")
    elif phase8_page == "Lesson 8.3":
        st.header("📚 Lesson 8.3: Custom Estimators & Compatibility")
        st.markdown("""
## Custom Estimators
Custom transformers and estimators must implement scikit-learn's API to plug into pipelines.

### Example transformer
```python
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return np.log1p(X)
```

### Example estimator
```python
from sklearn.base import BaseEstimator

class SimpleClassifier(BaseEstimator):
    def fit(self, X, y):
        self.mean_ = y.mean()
        return self
    def predict(self, X):
        return np.full(len(X), int(self.mean_ > 0.5))
```

### Validation
Use `check_estimator` or `sklearn.utils.estimator_checks` to validate API compatibility.

### Pipeline integration
- Implement `get_params()` and `set_params()` for compatibility
- Use `clone(estimator)` when copying models for grid search
- Custom transformers work best when wrapped in `Pipeline`
""")
        st.code("""from sklearn.utils.estimator_checks import check_estimator

check_estimator(LogTransformer())
""", language='python')
        render_lesson_complete_button("phase8", "8.3", 200, key="p8_lesson3_complete")
    elif phase8_page == "Quiz":
        st.header("❓ Phase 8 Quiz")
        if phase8_questions:
            for idx, q in enumerate(phase8_questions, 1):
                st.markdown(f"### Q{idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p8_q{q['id']}")
                if st.button("Submit", key=f"p8_submit_{q['id']}"):
                    correct = normalize_quiz_answer(q, selected)
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        save_quiz("phase8", q['id'], selected, True, q['xp'])
                    else:
                        st.error("❌ Incorrect")
                    st.info(q["explanation"])
                st.markdown("---")
        else:
            st.info("No Phase 8 quiz questions found yet.")
    elif phase8_page == "Code Challenges":
        st.header("💻 Phase 8 Code Challenges")
        if phase8_challenges:
            for challenge in phase8_challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p8_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase8", challenge['id'], challenge.get('xp', 100), key=f"p8_complete_{challenge['id']}")
        else:
            st.info("No Phase 8 challenges found yet.")

# ============================================
# PHASE 9: DEEP LEARNING OVERVIEW
# ============================================

elif phase_select == "🔴 Phase 9: Deep Learning Overview":
    st.title("🔴 Phase 9: Deep Learning Overview")
    phase9_page = st.sidebar.radio("Phase 9:", [
        "Overview",
        "Lesson 9.1",
        "Lesson 9.2",
        "Lesson 9.3",
        "Quiz",
        "Code Challenges"
    ])
    if phase9_page == "Overview":
        st.markdown("""
        ## Phase 9: Deep Learning Overview

        This phase introduces practical choices for deep learning, transfer learning, and model selection.

        **Topics include:**
        - When to use TensorFlow or PyTorch vs scikit-learn
        - Transfer learning and pretrained models
        - Best practices for data pipelines and evaluation
        - Using `MLPClassifier` as a bridge from scikit-learn to deep learning
        """)
    elif phase9_page == "Lesson 9.1":
        st.header("📚 Lesson 9.1: Deep Learning Decision Framework")
        st.markdown("""
## When to Use Deep Learning
Deep learning is best for unstructured data, representation learning, and complex feature extraction.

### Use deep learning when:
- Data is images, text, audio, or other unstructured formats
- You need learned features instead of manual engineering
- You have sufficient data or strong transfer learning resources

### Use scikit-learn when:
- Data is tabular or low-dimensional
- Interpretability and quick iteration matter
- You need low compute and fast prototyping

### Scikit-learn as a bridge
- `MLPClassifier` can be a good first step for simple neural networks
- It keeps training and evaluation inside the familiar scikit-learn API
- Use deep learning only when scikit-learn models cannot achieve the required performance

### Decision checklist
- Is the data mostly tabular? → scikit-learn
- Do you need clear feature importances? → scikit-learn
- Do you need end-to-end raw input modeling? → deep learning
""")
        render_lesson_complete_button("phase9", "9.1", 200, key="p9_lesson1_complete")
    elif phase9_page == "Lesson 9.2":
        st.header("📚 Lesson 9.2: Transfer Learning Basics")
        st.markdown("""
## Transfer Learning
Transfer learning reuses a pretrained network as a starting point for a new task.

### Common workflow
1. Load a pretrained backbone
2. Freeze base layers
3. Add a new task-specific head
4. Fine-tune on your dataset

### When to use transfer learning
- Small labeled datasets
- Vision or NLP tasks with pretrained backbones
- Need faster convergence and stronger generalization

### Why it helps
- Faster convergence
- Better performance with fewer labeled examples
- Leverages general features from large datasets

### Choosing a framework
- Use Keras/TensorFlow for rapid prototyping and accessible APIs
- Use PyTorch for more flexible custom training loops
- Use scikit-learn MLPs for smaller tabular tasks before moving to deep learning

### Practical caution
- Freeze base layers first, then fine-tune only if you have enough data
- Always validate on a separate held-out set to avoid overfitting the pretrained head
""")
        st.code("""from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base.trainable = False
x = base.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
predictions = layers.Dense(10, activation='softmax')(x)
model = models.Model(inputs=base.input, outputs=predictions)
""", language='python')
        render_lesson_complete_button("phase9", "9.2", 200, key="p9_lesson2_complete")
    elif phase9_page == "Lesson 9.3":
        st.header("📚 Lesson 9.3: Model Evaluation for Deep Learning")
        st.markdown("""
## Deep Learning Evaluation
Evaluate deep learning models with validation sets, early stopping, and robust metrics.

### Best practices
- Use validation data or cross-validation
- Monitor training and validation loss
- Save the best model with `ModelCheckpoint`
- Compare training and validation metrics to detect overfitting

### Early stopping
Stop training when validation performance stops improving.

```python
from tensorflow.keras.callbacks import EarlyStopping
early = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
```

### Metrics
- Accuracy for balanced classification
- AUC for ranking tasks
- Precision/Recall for imbalanced data

### Evaluation workflow
1. Track `val_loss` and `val_accuracy`
2. Use callbacks to save the best model
3. Compare metrics on a held-out test set after training
""")
        st.code("""from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

callbacks = [
    EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True),
    ModelCheckpoint('best_model.h5', save_best_only=True)
]
""", language='python')
        render_lesson_complete_button("phase9", "9.3", 200, key="p9_lesson3_complete")
    elif phase9_page == "Quiz":
        st.header("❓ Phase 9 Quiz")
        if phase9_questions:
            for idx, q in enumerate(phase9_questions, 1):
                st.markdown(f"### Q{idx}: {q['question']}")
                selected = st.radio("", q["options"], key=f"p9_q{q['id']}")
                if st.button("Submit", key=f"p9_submit_{q['id']}"):
                    correct = normalize_quiz_answer(q, selected)
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        save_quiz("phase9", q['id'], selected, True, q['xp'])
                    else:
                        st.error("❌ Incorrect")
                    st.info(q["explanation"])
                st.markdown("---")
        else:
            st.info("No Phase 9 quiz questions found yet.")
    elif phase9_page == "Code Challenges":
        st.header("💻 Phase 9 Code Challenges")
        if phase9_challenges:
            for challenge in phase9_challenges:
                with st.expander(f"{challenge['title']} - {challenge['difficulty']} ({challenge['xp']} XP)"):
                    st.write(challenge["description"])
                    st.code(challenge["starter_code"], language='python')
                    if st.button("Show Solution", key=f"p9_sol_{challenge['id']}"):
                        st.code(challenge["solution"], language='python')
                    st.markdown("**Hints:**")
                    for hint in challenge["hints"]:
                        st.write(f"💡 {hint}")
                    render_challenge_complete_button("phase9", challenge['id'], challenge.get('xp', 100), key=f"p9_complete_{challenge['id']}")
        else:
            st.info("No Phase 9 challenges found yet.")

# ============================================
# SCITKIT-LEARN CHECKLIST
# ============================================

elif phase_select == "📋 Scikit-Learn Checklist":
    st.title("📋 Scikit-Learn Checklist")
    st.markdown("""
    This checklist maps the current curriculum coverage against missing scikit-learn topics for Phases 3-9.
    Use it to identify next scaffolding work and track gaps in lessons, quizzes, and challenges.
    """)

    coverage = [
        {
            'phase': 'Phase 3',
            'focus': 'Core API, Pipelines, ColumnTransformer, GridSearchCV',
            'lessons': 3,
            'quiz': len(phase3_questions),
            'challenges': len(phase3_challenges),
            'status': 'Covered, expand custom pipeline and feature engineering scenarios'
        },
        {
            'phase': 'Phase 4',
            'focus': 'Regression, Classification, Ensembles, Thresholding',
            'lessons': 3,
            'quiz': len(phase4_questions),
            'challenges': len(phase4_challenges),
            'status': 'Covered, add stacking and model interpretation challenges'
        },
        {
            'phase': 'Phase 5',
            'focus': 'Clustering, PCA, Manifold Learning, Anomaly Detection',
            'lessons': 3,
            'quiz': len(phase5_questions),
            'challenges': len(phase5_challenges),
            'status': 'Covered, expanded with manifold methods and stronger anomaly detection examples'
        },
        {
            'phase': 'Phase 6',
            'focus': 'Metrics, CV, Feature Selection, Calibration',
            'lessons': 3,
            'quiz': len(phase6_questions),
            'challenges': len(phase6_challenges),
            'status': 'Covered, add nested CV and calibration visuals'
        },
        {
            'phase': 'Phase 8',
            'focus': 'Incremental learning, explainability, custom estimators',
            'lessons': 3,
            'quiz': len(phase8_questions),
            'challenges': len(phase8_challenges),
            'status': 'Scaffolded, expand edge topic examples and time series support'
        },
        {
            'phase': 'Phase 9',
            'focus': 'Deep learning decision framework, transfer learning, evaluation',
            'lessons': 3,
            'quiz': len(phase9_questions),
            'challenges': len(phase9_challenges),
            'status': 'Scaffolded, add concrete Keras/PyTorch primer and deployment guidance'
        }
    ]

    st.markdown("### Phase Coverage Summary")
    for entry in coverage:
        st.markdown(f"**{entry['phase']}** — {entry['focus']}  ")
        st.markdown(f"- Lessons: {entry['lessons']}  ")
        st.markdown(f"- Quiz items: {entry['quiz']}  ")
        st.markdown(f"- Challenges: {entry['challenges']}  ")
        st.markdown(f"- Status: {entry['status']}  ")
        st.markdown("---")

    st.markdown("### Missing / Next Work")
    st.markdown("""
    - Phase 3: Add `FeatureUnion`, `TransformedTargetRegressor`, custom pipeline debugging, and pipeline + GridSearchCV case studies.
    - Phase 4: Add stacking/voting ensembles, model interpretation, threshold tuning, and regression residual diagnostics.
    - Phase 5: Expand spectral clustering, autoencoder-based reduction, and density-based anomaly use cases.
    - Phase 6: Add nested cross-validation, multi-metric model comparison, calibration curves, and precision/recall threshold tuning challenges.
    - Phase 8: Add time series pipeline patterns, out-of-core preprocessing, online model monitoring, and explainability examples for production drift.
    - Phase 9: Add concrete Keras/PyTorch demos, transfer learning end-to-end workflow, and deep learning evaluation best practices.
    """)

    st.markdown("### Scikit-Learn Topic Tracker")
    st.markdown("""
    - [x] Pipeline / ColumnTransformer / feature engineering
    - [x] GridSearchCV / RandomizedSearchCV / cross_val_score
    - [x] Regression and classification models
    - [x] Ensemble methods (Random Forest, Gradient Boosting)
    - [ ] Stacking / Voting / advanced ensembles
    - [x] Clustering and PCA
    - [x] Manifold methods (t-SNE / UMAP)
    - [ ] Nested CV and model selection workflows
    - [ ] Time series and incremental model pipelines
    - [ ] Keras/PyTorch deep learning primer and transfer learning
    """)

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>🚀 ML Learning Hub | Phases 1-6 | Complete Learning Path | v2.1</small>
</div>
""", unsafe_allow_html=True)