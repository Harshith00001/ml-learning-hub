import streamlit as st
import pandas as pd
import json
import sqlite3
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="ML Learning Hub - Phase 1", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE FUNCTIONS
# ============================================

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_progress
                 (id INTEGER PRIMARY KEY, 
                  lesson_id TEXT, 
                  completed BOOLEAN, 
                  xp INTEGER, 
                  date TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_results
                 (id INTEGER PRIMARY KEY, 
                  question_id INTEGER, 
                  user_answer TEXT, 
                  correct BOOLEAN, 
                  xp_earned INTEGER, 
                  date TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS code_challenges
                 (id INTEGER PRIMARY KEY, 
                  challenge_id INTEGER, 
                  completed BOOLEAN, 
                  xp_earned INTEGER, 
                  date TEXT)''')
    
    conn.commit()
    conn.close()

def save_progress(lesson_id, xp):
    """Save lesson completion"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('''INSERT INTO user_progress (lesson_id, completed, xp, date)
                 VALUES (?, ?, ?, ?)''',
              (lesson_id, True, xp, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def save_quiz_result(question_id, user_answer, correct, xp):
    """Save quiz result"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('''INSERT INTO quiz_results (question_id, user_answer, correct, xp_earned, date)
                 VALUES (?, ?, ?, ?, ?)''',
              (question_id, user_answer, correct, xp, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_total_xp():
    """Calculate total XP earned"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('SELECT SUM(xp_earned) FROM quiz_results WHERE correct = 1')
    result = c.fetchone()[0]
    conn.close()
    return result if result else 0

def get_completed_lessons():
    """Get number of completed lessons"""
    conn = sqlite3.connect('database/progress.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(DISTINCT lesson_id) FROM user_progress WHERE completed = 1')
    result = c.fetchone()[0]
    conn.close()
    return result

def load_mcq_questions():
    """Load MCQ questions from JSON"""
    try:
        with open('challenges/mcq/phase1_questions.json', 'r') as f:
            return json.load(f)
    except:
        return {"phase1_fundamentals": []}

def load_code_challenges():
    """Load code challenges from JSON"""
    try:
        with open('challenges/code/phase1_challenges.json', 'r') as f:
            return json.load(f)
    except:
        return {"phase1_code_challenges": []}

# ============================================
# INITIALIZE
# ============================================

init_db()
st.session_state.setdefault('current_xp', get_total_xp())

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("🎮 ML Learning Hub")
st.sidebar.markdown("### Phase 1: ML Fundamentals")

page = st.sidebar.radio("Select Section:", [
    "📊 Dashboard",
    "📚 Lesson 1.1",
    "📚 Lesson 1.2",
    "📚 Lesson 1.3",
    "❓ Quiz",
    "💻 Code Challenges",
    "📈 Progress"
])

st.sidebar.markdown("---")
total_xp = st.session_state.current_xp
st.sidebar.metric("Total XP", f"{total_xp:,}", delta=None)
st.sidebar.metric("Lessons Completed", get_completed_lessons())

st.sidebar.markdown("---")
st.sidebar.markdown("**Resources:**")
st.sidebar.markdown("[📖 Scikit-Learn Docs](https://scikit-learn.org/)")
st.sidebar.markdown("[🐼 Pandas Docs](https://pandas.pydata.org/)")
st.sidebar.markdown("[📊 NumPy Docs](https://numpy.org/)")

# ============================================
# DASHBOARD PAGE
# ============================================

if page == "📊 Dashboard":
    st.title("🎯 Dashboard - Phase 1: ML Fundamentals")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🏆 Total XP",
            f"{get_total_xp()}",
            "+150 this week"
        )
    
    with col2:
        st.metric(
            "🎖️ Badges Earned",
            3,
            "Beginner, Learner, Questioner"
        )
    
    with col3:
        st.metric(
            "🔥 Current Streak",
            "5 days",
            "Keep it up!"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Learning Path Progress")
        progress_data = {
            "Section": ["1.1: Basics", "1.2: Types", "1.3: Concepts", "Quiz", "Challenges"],
            "Progress": [100, 100, 50, 0, 0]
        }
        df_progress = pd.DataFrame(progress_data)
        fig = px.bar(df_progress, x="Section", y="Progress", 
                     title="Phase 1 Completion %",
                     labels={"Progress": "Completion %"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏅 Achievements")
        achievements = [
            "✅ Python Novice - Complete Python Basics",
            "✅ Curious Learner - Complete 2 lessons",
            "🔒 Quiz Master - Score 80%+ on Quiz",
            "🔒 Code Wizard - Complete 3 challenges",
            "🔒 Phase Complete - Finish all Phase 1 content"
        ]
        for achievement in achievements:
            st.write(achievement)
    
    st.markdown("---")
    st.subheader("📖 Next Steps")
    st.info("""
    1. ✅ Complete Lesson 1.1: What is ML?
    2. ✅ Complete Lesson 1.2: Types of ML
    3. 📍 **Currently**: Work on Lesson 1.3
    4. ⭕ Take the Phase 1 Quiz
    5. ⭕ Complete Code Challenges
    """)

# ============================================
# LESSON 1.1
# ============================================

elif page == "📚 Lesson 1.1":
    st.title("📚 Lesson 1.1: What is Machine Learning?")
    
    tabs = st.tabs(["📖 Content", "🎥 Visualization", "✅ Complete", "💡 Tips"])
    
    with tabs[0]:
        st.markdown("""
## What is Machine Learning?

### Definition
Machine Learning is a branch of **Artificial Intelligence** that enables computer systems to learn and improve from experience without being explicitly programmed.

---

## Traditional Programming vs Machine Learning

### Traditional Programming
```
Rules + Data → Program → Output
```
Programmer writes all rules manually.

### Machine Learning
```
Data + Outputs → Algorithm → Rules
```
Algorithm discovers rules automatically!

---

## Example: Email Spam Detection

### Traditional Approach ❌
```python
if "Buy now!" in email:
    return "SPAM"
if contains_link and unknown_sender:
    return "SPAM"
# ... hundreds more rules!
```
Problem: Every new spam trick needs new rules!

### Machine Learning Approach ✅
```python
# Model learns from examples
model.fit(training_emails, labels)
prediction = model.predict(new_email)
# Automatically adapts!
```

---

## Why Machine Learning?

### 1. **Automation** 🤖
- Automatically discover patterns
- Reduce manual programming

### 2. **Scalability** 📈
- Handle complex patterns
- Work with huge datasets

### 3. **Adaptability** 🔄
- Improve over time
- Learn new patterns

### 4. **Efficiency** ⚡
- Faster than manual rules
- Better performance

---

## Real-World Applications

| Application | Use Case |
|-------------|----------|
| 📧 Email | Spam detection |
| 🎬 Netflix | Recommendations |
| 🗣️ Voice Assistants | Speech recognition |
| 🚗 Autonomous Vehicles | Object detection |
| 🏥 Healthcare | Disease diagnosis |
| 💰 Banking | Fraud detection |
| 📱 Social Media | Face recognition |

---

## Key Takeaway

Machine Learning enables computers to **learn from data** instead of following explicitly programmed rules. This makes systems more flexible, scalable, and powerful!

        """)
    
    with tabs[1]:
        st.subheader("Traditional vs Machine Learning")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Traditional Programming")
            st.markdown("""
```
┌─────────────┐
│  Rules      │
│ (Hardcoded) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Program    │
└──────┬──────┘
       │
   ┌───┴───┐
   ↓       ↓
 Data   Output
```
            """)
        
        with col2:
            st.write("### Machine Learning")
            st.markdown("""
```
┌─────────────┐
│  Data       │
│ + Labels    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Algorithm   │
│ (Learning)  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Model     │
│  (Rules)    │
└─────────────┘
```
            """)
    
    with tabs[2]:
        st.success("✅ Lesson 1.1 Completed!")
        st.balloons()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("XP Earned", "+100 XP", "")
        with col2:
            st.metric("Time Spent", "~45 min", "")
        
        if st.button("Mark as Complete & Continue"):
            save_progress("1.1", 100)
            st.session_state.current_xp += 100
            st.success("Great! Move to Lesson 1.2")
    
    with tabs[3]:
        st.markdown("""
### 💡 Tips for Understanding

1. **Think Practically**: Consider email spam. Traditional rules fail quickly; ML learns!
2. **Key Concept**: ML is about learning PATTERNS from DATA
3. **Real Applications**: Think about Netflix, Google Translate, Siri - all use ML
4. **Next**: We'll explore different types of ML approaches

### 📝 Key Terms to Remember
- **Data**: Information we learn from
- **Pattern**: Rules the algorithm discovers
- **Model**: The result of learning
- **Prediction**: What our model outputs
        """)

# ============================================
# LESSON 1.2
# ============================================

elif page == "📚 Lesson 1.2":
    st.title("📚 Lesson 1.2: Three Types of Machine Learning")
    
    tabs = st.tabs(["📖 Content", "📊 Comparison", "🎯 Examples", "✅ Complete"])
    
    with tabs[0]:
        st.markdown("""
## Types of Machine Learning

### 1️⃣ Supervised Learning
**Learning from labeled data**

#### Characteristics:
- ✅ Training data has labels/answers
- ✅ Learn to map Input → Output
- ✅ Clear right/wrong answers

#### Two Types:

**A) Regression** - Predict numbers
```
Input: House features (size, bedrooms)
Output: Price (continuous value)
```

**B) Classification** - Predict categories
```
Input: Email content
Output: Spam or Not Spam (category)
```

#### Examples:
- 🏠 House price prediction
- 📧 Email spam classification
- 🏥 Disease diagnosis
- 🎬 Movie rating prediction

---

### 2️⃣ Unsupervised Learning
**Finding patterns in unlabeled data**

#### Characteristics:
- ❌ No labels/answers provided
- ✅ Discover hidden patterns
- ✅ Explore data structure

#### Two Types:

**A) Clustering** - Group similar items
```
Input: Customer data (no labels)
Output: 3 groups of customers
```

**B) Dimensionality Reduction** - Simplify data
```
Input: 1000 features
Output: 50 important features
```

#### Examples:
- 👥 Customer segmentation
- 📰 Document clustering
- 🔬 Gene sequencing
- 🗺️ Market segmentation

---

### 3️⃣ Reinforcement Learning
**Learning through rewards & penalties**

#### Characteristics:
- 🤖 Agent interacts with environment
- 🏆 Receives rewards for good actions
- ❌ Receives penalties for bad actions

#### How it works:
```
Agent takes action
       ↓
Environment responds
       ↓
Agent gets reward/penalty
       ↓
Agent learns optimal strategy
```

#### Examples:
- 🎮 Game playing (Chess, Go, Video games)
- 🤖 Robot control
- 🚗 Autonomous driving
- 💰 Trading strategies

        """)
    
    with tabs[1]:
        st.subheader("Comparison Table")
        
        comparison_df = pd.DataFrame({
            "Aspect": ["Data Type", "Labels", "Goal", "Example Task"],
            "Supervised": ["Labeled", "Yes ✅", "Predict", "House price"],
            "Unsupervised": ["Unlabeled", "No ❌", "Explore", "Clustering"],
            "Reinforcement": ["Experience", "N/A", "Reward Maximize", "Game AI"]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
### Supervised Learning
- **When**: You have labeled data
- **Want**: Predict specific values
- **Use Cases**: Classification, Regression
- **Example**: Train model to recognize cats/dogs
            """)
        
        with col2:
            st.markdown("""
### Unsupervised Learning
- **When**: You have unlabeled data
- **Want**: Discover patterns
- **Use Cases**: Clustering, Grouping
- **Example**: Find customer segments automatically
            """)
        
        with col3:
            st.markdown("""
### Reinforcement Learning
- **When**: Agent learns through interaction
- **Want**: Maximize rewards
- **Use Cases**: Game AI, Robotics
- **Example**: Train agent to play chess
            """)
    
    with tabs[2]:
        st.subheader("Real-World Examples")
        
        examples = {
            "🛍️ E-Commerce Recommendation": {
                "Type": "Supervised (Classification)",
                "Data": "Past purchases, browsing history (labeled)",
                "Output": "Recommend products you'll buy"
            },
            "🎵 Spotify Playlist Creation": {
                "Type": "Unsupervised (Clustering)",
                "Data": "Song characteristics (no labels)",
                "Output": "Group similar songs into playlists"
            },
            "🎮 Game AI": {
                "Type": "Reinforcement Learning",
                "Data": "Game states & actions",
                "Output": "Agent learns winning strategies"
            },
            "🏥 Medical Diagnosis": {
                "Type": "Supervised (Classification)",
                "Data": "Symptoms & diagnoses (labeled)",
                "Output": "Predict disease from symptoms"
            },
            "👥 Social Media Groups": {
                "Type": "Unsupervised (Clustering)",
                "Data": "User behavior (no labels)",
                "Output": "Find communities/groups"
            }
        }
        
        for title, details in examples.items():
            with st.expander(f"**{title}**"):
                st.write(f"**Type**: {details['Type']}")
                st.write(f"**Data**: {details['Data']}")
                st.write(f"**Output**: {details['Output']}")
    
    with tabs[3]:
        st.success("✅ Lesson 1.2 Completed!")
        st.balloons()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("XP Earned", "+100 XP")
        with col2:
            st.metric("Time Spent", "~60 min")
        
        if st.button("Mark Complete & Continue"):
            save_progress("1.2", 100)
            st.session_state.current_xp += 100
            st.success("Excellent! Ready for Lesson 1.3?")

# ============================================
# LESSON 1.3
# ============================================

elif page == "📚 Lesson 1.3":
    st.title("📚 Lesson 1.3: Key Concepts & Terminology")
    
    tabs = st.tabs(["📖 Content", "🔍 Deep Dive", "📊 Visualization", "✅ Complete"])
    
    with tabs[0]:
        st.markdown("""
## Key Concepts Every ML Beginner Must Know

### 1. Features (X) and Target (y)

**Features (X)**: Input variables
```
House Features: [Size, Bedrooms, Bathrooms, Location]
```

**Target (y)**: Output we predict
```
Target: House Price
```

#### Example:
```
Features (X):          Target (y):
[2000, 3, 2, Downtown] → $500,000
[1500, 2, 1, Suburb]   → $350,000
[3500, 4, 3, Downtown] → $750,000
```

---

### 2. Train-Test Split

**Training Set (70-80%)**
- Data used to train the model
- Model learns patterns from this

**Test Set (20-30%)**
- Data to evaluate model
- **Important**: Model hasn't seen this before!

#### Why Split?
```
Without Split:
- Model memorizes training data
- Fails on new data
- Can't measure real performance

With Split:
- Know true performance
- Detect overfitting
- Reliable predictions on new data
```

---

### 3. Overfitting vs Underfitting

#### Overfitting ❌
- Model learns training data TOO well
- Memorizes noise/quirks
- Bad on new data

```
Training: 99% accurate
Test: 60% accurate  ← HUGE GAP!
```

**Causes**: Too complex model, too much training time

**Solutions**: Simpler model, more data, regularization

#### Underfitting ❌
- Model is TOO SIMPLE
- Can't learn patterns
- Bad on both train and test

```
Training: 70% accurate
Test: 68% accurate  ← Both poor!
```

**Causes**: Simple model, not enough training

**Solutions**: More complex model, train longer

#### Perfect Fit ✅
```
Training: 85% accurate
Test: 83% accurate  ← Similar and good!
```

---

### 4. Accuracy & Other Metrics

**Accuracy**
```
Accuracy = Correct Predictions / Total Predictions
```

Example:
- 95 correct out of 100 = 95% accuracy

---

### 5. Cross-Validation

Instead of one train-test split, use multiple!

```
Data → Split 1 → Train/Test
    → Split 2 → Train/Test
    → Split 3 → Train/Test
    
Average the results for better estimate
```

**Benefit**: More reliable performance estimate

        """)
    
    with tabs[1]:
        st.subheader("🔍 Deep Dive: Overfitting")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Good Model**")
            st.markdown("""
```
Training Error:   15%
Test Error:       16%
Difference:       1%  ✅
```

The model generalizes well!
            """)
        
        with col2:
            st.write("**Overfitted Model**")
            st.markdown("""
```
Training Error:   2%
Test Error:       30%
Difference:       28%  ❌
```

Model memorized training noise!
            """)
        
        st.info("""
### How to Prevent Overfitting?

1. **Use more training data**
   - More examples help avoid memorization
   
2. **Simpler model**
   - Fewer parameters to memorize
   
3. **Regularization**
   - Penalty for complex models
   
4. **Early stopping**
   - Stop training when test error increases
   
5. **Cross-validation**
   - Multiple train-test splits
        """)
    
    with tabs[2]:
        st.subheader("📊 Model Performance Visualization")
        
        # Create visualization data
        epochs = list(range(1, 21))
        train_loss = [0.8 - (0.8 * (i/20)**1.5) + 0.01 * i for i in range(1, 21)]
        test_loss = [0.8 - (0.7 * (i/20)**1.2) + 0.05 * (i/20)**2 for i in range(1, 21)]
        
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=epochs, y=train_loss, 
                                mode='lines+markers', name='Training Loss'))
        fig.add_trace(go.Scatter(x=epochs, y=test_loss, 
                                mode='lines+markers', name='Test Loss'))
        
        fig.update_layout(
            title="Training vs Test Loss (Overfitting Example)",
            xaxis_title="Epoch",
            yaxis_title="Loss",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("📝 Notice how training loss keeps decreasing, but test loss increases after epoch 12 - classic overfitting!")
    
    with tabs[3]:
        st.success("✅ Lesson 1.3 Completed!")
        st.balloons()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("XP Earned", "+100 XP")
        with col2:
            st.metric("Progress", "50%", "→ Quiz time!")
        
        if st.button("Mark Complete"):
            save_progress("1.3", 100)
            st.session_state.current_xp += 100
            st.success("🎉 All lessons complete! Take the quiz next!")

# ============================================
# QUIZ PAGE
# ============================================

elif page == "❓ Quiz":
    st.title("❓ Phase 1 Quiz - Test Your Knowledge!")
    
    st.info("Answer all questions correctly to earn 100 XP and unlock Code Challenges")
    
    mcq_data = load_mcq_questions()
    questions = mcq_data.get("phase1_fundamentals", [])
    
    if questions:
        quiz_score = 0
        total_questions = len(questions)
        
        for idx, q in enumerate(questions, 1):
            st.markdown(f"### Question {idx}/{total_questions}")
            st.write(q["question"])
            
            selected = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"q_{q['id']}"
            )
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button(f"Submit Answer {idx}", key=f"submit_{q['id']}"):
                    correct = selected[0] == q["correct"]
                    
                    if correct:
                        st.success(f"✅ Correct! +{q['xp']} XP")
                        quiz_score += q["xp"]
                    else:
                        st.error(f"❌ Incorrect")
                    
                    st.info(f"**Explanation**: {q['explanation']}")
                    save_quiz_result(q['id'], selected, correct, q['xp'] if correct else 0)
            
            with col2:
                difficulty_color = {
                    "Easy": "🟢",
                    "Medium": "🟡",
                    "Hard": "🔴"
                }
                st.write(f"{difficulty_color.get(q['difficulty'])} {q['difficulty']}")
            
            st.markdown("---")

# ============================================
# CODE CHALLENGES PAGE
# ============================================

elif page == "💻 Code Challenges":
    st.title("💻 Code Challenges - Phase 1")
    
    challenges_data = load_code_challenges()
    challenges = challenges_data.get("phase1_code_challenges", [])
    
    st.write("Complete code challenges to apply what you learned!")
    
    for challenge in challenges:
        with st.expander(f"**{challenge['title']}** - {challenge['difficulty']}", expanded=False):
            st.write(f"**Description**: {challenge['description']}")
            st.write(f"**XP Reward**: {challenge['xp']} XP")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Starter Code**:")
                st.code(challenge['starter_code'], language='python')
            
            with col2:
                st.write("**Hints**:")
                for hint in challenge['hints']:
                    st.write(f"💡 {hint}")
            
            st.write("---")
            
            code_input = st.text_area(
                "Write your solution:",
                height=250,
                key=f"code_{challenge['id']}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Submit Solution", key=f"submit_code_{challenge['id']}"):
                    st.info("🔍 Code evaluation running... (Coming soon in enhanced version)")
            
            with col2:
                if st.button(f"Show Solution", key=f"show_{challenge['id']}"):
                    with st.expander("Solution:"):
                        st.code(challenge['solution'], language='python')

# ============================================
# PROGRESS PAGE
# ============================================

elif page == "📈 Progress":
    st.title("📈 Your Progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total XP", get_total_xp())
    with col2:
        st.metric("Lessons Done", get_completed_lessons(), f"of 3")
    with col3:
        st.metric("Quiz Questions", "0 of 6", "Not started")
    with col4:
        st.metric("Code Challenges", "0 of 4", "Locked")
    
    st.markdown("---")
    
    st.subheader("📚 Lesson Progress")
    lesson_progress = pd.DataFrame({
        "Lesson": ["1.1: What is ML", "1.2: Types of ML", "1.3: Key Concepts"],
        "Status": ["✅ Complete", "✅ Complete", "✅ Complete"],
        "XP": [100, 100, 100]
    })
    st.dataframe(lesson_progress, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🎖️ Badges")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("✅ **Beginner**")
        st.write("Complete Lesson 1.1")
    with col2:
        st.write("✅ **Curious Learner**")
        st.write("Complete 2 lessons")
    with col3:
        st.write("🔒 **Quiz Master**")
        st.write("Score 80%+ on quiz")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>🚀 ML Learning Hub | Phase 1: ML Fundamentals | v1.0</small>
</div>
""", unsafe_allow_html=True)