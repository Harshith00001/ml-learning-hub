import streamlit as st
import pandas as pd
import json
import sqlite3
from datetime import datetime
import plotly.express as px
from lessons.phase2_lessons import get_lesson

st.set_page_config(page_title="ML Learning Hub - Phase 2", layout="wide")

def init_db():
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS phase2_progress
                 (id INTEGER PRIMARY KEY,
                  lesson_id TEXT,
                  completed BOOLEAN,
                  xp INTEGER,
                  date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS phase2_quiz
                 (id INTEGER PRIMARY KEY,
                  question_id INTEGER,
                  answer TEXT,
                  correct BOOLEAN,
                  xp INTEGER,
                  date TEXT)''')
    conn.commit()
    conn.close()

def save_progress(lesson_id, xp):
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('INSERT INTO phase2_progress (lesson_id, completed, xp, date) VALUES (?, ?, ?, ?)',
              (lesson_id, True, xp, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def save_quiz(question_id, answer, correct, xp):
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('INSERT INTO phase2_quiz (question_id, answer, correct, xp, date) VALUES (?, ?, ?, ?, ?)',
              (question_id, answer, correct, xp, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_total_xp():
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('SELECT SUM(xp) FROM phase2_progress')
    lesson_xp = c.fetchone()[0] or 0
    c.execute('SELECT SUM(xp) FROM phase2_quiz')
    quiz_xp = c.fetchone()[0] or 0
    conn.close()
    return lesson_xp + quiz_xp

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

init_db()
st.session_state.setdefault('phase2_xp', get_total_xp())

st.sidebar.title("🎯 Phase 2: Scikit-Learn Basics")
page = st.sidebar.radio("Navigate:", [
    "Overview",
    "Lesson 2.1",
    "Lesson 2.2",
    "Lesson 2.3",
    "Quiz",
    "Code Challenges",
    "Progress"
])
st.sidebar.markdown("---")
st.sidebar.metric("Total XP", st.session_state.phase2_xp)
st.sidebar.markdown("Run with:")
st.sidebar.code("streamlit run app_phase2.py")

if page == "Overview":
    st.title("Phase 2: Scikit-Learn Basics")
    st.write("Deepen your scikit-learn skills with preprocessing, pipelines, and model validation.")
    st.markdown("""
- ✅ Estimator pattern
- ✅ Feature scaling
- ✅ Pipelines
- ✅ Train/test split
- ✅ Cross-validation
- ✅ Hyperparameter tuning
""")
    progress = pd.DataFrame({
        "Topic": ["Core Concepts", "Preprocessing", "Validation", "Quiz", "Challenges"],
        "Status": ["Ready", "Ready", "Ready", "Ready", "Ready"]
    })
    st.table(progress)
    st.markdown("### Visual guide")
    chart = px.bar(
        progress,
        x="Topic",
        y=[1, 1, 1, 1, 1],
        labels={"y": "Ready"},
        text_auto=True
    )
    st.plotly_chart(chart, use_container_width=True)

def render_lesson(lesson_id):
    lesson = get_lesson(lesson_id)
    if lesson is None:
        st.error("Lesson content not found.")
        return

    st.header(f"{lesson_id} — {lesson['title']}")
    tabs = st.tabs(["📖 Lesson", "💻 Example", "🧠 Key Ideas", "✅ Complete"])

    with tabs[0]:
        st.markdown(lesson["content"])

    with tabs[1]:
        if lesson_id == "2.1":
            st.markdown("```python\nfrom sklearn.datasets import load_iris\nfrom sklearn.tree import DecisionTreeClassifier\n\niris = load_iris()\nX, y = iris.data, iris.target\nmodel = DecisionTreeClassifier()\nmodel.fit(X, y)\nprint(model.score(X, y))\n```")
            iris = load_json if False else None
        elif lesson_id == "2.2":
            st.markdown("```python\nfrom sklearn.preprocessing import StandardScaler\n\nscaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)\nprint(X_scaled.mean(axis=0))\nprint(X_scaled.std(axis=0))\n```")
        elif lesson_id == "2.3":
            st.markdown("```python\nfrom sklearn.model_selection import train_test_split, cross_val_score\nfrom sklearn.linear_model import LogisticRegression\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nmodel = LogisticRegression(max_iter=200)\nscores = cross_val_score(model, X, y, cv=5)\nprint(scores)\n```")
    with tabs[2]:
        if lesson_id == "2.1":
            st.write("- scikit-learn uses a consistent estimator API")
            st.write("- `fit` trains, `predict` generates output, `score` measures performance")
            st.write("- The library includes data sets and tools for nearly every basic ML workflow")
        elif lesson_id == "2.2":
            st.write("- Scaling helps many models learn faster and perform better")
            st.write("- Pipelines keep preprocessing and modeling together")
            st.write("- Transformers should be fit only on training data")
        elif lesson_id == "2.3":
            st.write("- Use train/test split before model evaluation")
            st.write("- Cross-validation gives a stronger performance estimate")
            st.write("- Grid search finds better hyperparameters while avoiding overfitting")
    with tabs[3]:
        if st.button(f"Mark {lesson_id} Complete"):
            save_progress(lesson_id, 100)
            st.session_state.phase2_xp += 100
            st.success(f"{lesson['title']} completed! +100 XP")

if page == "Lesson 2.1":
    render_lesson("2.1")
elif page == "Lesson 2.2":
    render_lesson("2.2")
elif page == "Lesson 2.3":
    render_lesson("2.3")

elif page == "Quiz":
    st.title("📝 Phase 2 Quiz")
    questions = load_json('challenges/mcq/phase2_questions.json')['phase2_sklearn_basics']
    for q in questions:
        st.markdown(f"**{q['question']}**")
        selected = st.radio("", q["options"], key=q["id"])
        if st.button("Submit answer", key=f"submit_{q['id']}"):
            correct = selected[0] == q["correct"]
            if correct:
                st.success(f"Correct! +{q['xp']} XP")
                save_quiz(q["id"], selected, True, q["xp"])
                st.session_state.phase2_xp += q["xp"]
            else:
                st.error("Incorrect.")
                save_quiz(q["id"], selected, False, 0)
            st.info(q["explanation"])
        st.markdown("---")

elif page == "Code Challenges":
    st.title("💻 Phase 2 Code Challenges")
    challenges = load_json('challenges/code/phase2_challenges.json')['phase2_code_challenges']
    for challenge in challenges:
        with st.expander(f"{challenge['title']} ({challenge['difficulty']})", expanded=False):
            st.write(challenge["description"])
            st.code(challenge["starter_code"], language='python')
            if st.button("Show solution", key=f"solution_{challenge['id']}"):
                st.code(challenge["solution"], language='python')
            st.markdown("**Hints:**")
            for hint in challenge["hints"]:
                st.write(f"- {hint}")

elif page == "Progress":
    st.title("📈 Phase 2 Progress")
    st.metric("XP earned", st.session_state.phase2_xp)
    progress_table = pd.DataFrame([
        {"Lesson": "2.1 Core Concepts", "Status": "Ready"},
        {"Lesson": "2.2 Preprocessing", "Status": "Ready"},
        {"Lesson": "2.3 Validation", "Status": "Ready"},
    ])
    st.table(progress_table)
    st.write("Complete lessons and quizzes to unlock the next phase.")