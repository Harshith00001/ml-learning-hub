"""
Phase 1: ML Fundamentals - Lesson Content
"""

LESSONS = {
    "1.1": {
        "title": "What is Machine Learning?",
        "duration": "45 minutes",
        "content": """
# 1.1: What is Machine Learning?

## Definition
Machine Learning is a branch of Artificial Intelligence that enables computer systems to learn and improve from experience without being explicitly programmed.

## Key Points:
- **Traditional Programming**: Rules → Input → Output
- **Machine Learning**: Input + Output → Rules

## Example:
```
Traditional: IF age > 18 THEN adult = True
ML: Learn this rule from data automatically
```

## Why Machine Learning?
1. **Automation**: Automatically discover patterns
2. **Scalability**: Handle complex problems
3. **Adaptability**: Improve over time
4. **Efficiency**: Reduce manual programming

## Real-World Applications:
- 📧 Email spam detection
- 🎬 Netflix movie recommendations
- 🚗 Self-driving cars
- 🏥 Medical diagnosis
- 💰 Fraud detection
- 🎤 Voice assistants

## Key Takeaway:
Instead of programming every rule, we let algorithms learn patterns from data!
        """
    },
    "1.2": {
        "title": "Three Types of Machine Learning",
        "duration": "60 minutes",
        "content": """
# 1.2: Three Types of Machine Learning

## 1️⃣ Supervised Learning
**Learning from labeled data**

### Characteristics:
- Training data has labels/answers
- Algorithm learns to map Input → Output
- Requires labeled dataset

### Types:
- **Regression**: Predict continuous values
  - Examples: House price, temperature, stock price
  
- **Classification**: Predict categories
  - Examples: Spam/Not Spam, Cat/Dog, Disease/Healthy

### Example:
```
Data: (House, Price)
(Size: 2000 sq ft, Bedrooms: 3) → $500,000
(Size: 3000 sq ft, Bedrooms: 4) → $650,000
...
Task: Predict price of new house
```

---

## 2️⃣ Unsupervised Learning
**Finding patterns in unlabeled data**

### Characteristics:
- No labels/answers provided
- Algorithm finds hidden patterns
- Explores data structure

### Types:
- **Clustering**: Group similar items
  - Examples: Customer segmentation, document clustering
  
- **Dimensionality Reduction**: Reduce features
  - Examples: Feature extraction, data compression

### Example:
```
Data: Customer purchase history (no labels)
Algorithm groups customers by:
- High spenders
- Occasional buyers
- Window shoppers
```

---

## 3️⃣ Reinforcement Learning
**Learning through rewards and penalties**

### Characteristics:
- Agent learns by interacting with environment
- Receives rewards for good actions
- Receives penalties for bad actions

### Applications:
- Game playing (Chess, Go)
- Robotics
- Autonomous vehicles

### Example:
```
Agent learns to play Tic-Tac-Toe
- Win = +1 reward
- Loss = -1 reward
- Draw = 0 reward
Algorithm learns winning strategy
```

---

## Comparison Table:

| Aspect | Supervised | Unsupervised | Reinforcement |
|--------|-----------|-------------|--------------|
| **Labels** | Yes | No | N/A |
| **Goal** | Predict | Explore | Maximize reward |
| **Data** | Labeled | Unlabeled | Experience |
| **Examples** | Classification | Clustering | Game AI |

## Key Takeaway:
- **Supervised**: Learn from labeled examples
- **Unsupervised**: Discover hidden patterns
- **Reinforcement**: Learn from rewards
        """
    },
    "1.3": {
        "title": "Key Concepts & Terminology",
        "duration": "50 minutes",
        "content": """
# 1.3: Key Concepts & Terminology

## Features (X) & Target (y)
- **Features (X)**: Input variables used to make predictions
- **Target (y)**: Output variable we want to predict

Example:
```
Predicting House Price:
Features: [Size, Bedrooms, Location, Age]
Target: Price
```

---

## Training vs Testing

### Training Set (70-80%)
- Data used to train the model
- Model learns patterns from this data

### Test Set (20-30%)
- Data used to evaluate model performance
- **Important**: Model has never seen this data

### Why Split?
```
Without split:
- Model performs well on training data
- But fails on new data (overfitting)

With split:
- Know how model performs on unseen data
- Better estimate of real-world performance
```

---

## Overfitting & Underfitting

### Overfitting
- Model learns training data **too well**
- Memorizes noise and quirks
- Poor performance on new data
- **Solution**: Use more data, regularization, simpler model

```
Training Accuracy: 99%
Test Accuracy: 60%  ❌ Too much difference!
```

### Underfitting
- Model is **too simple**
- Can't capture patterns in data
- Poor performance on both train and test
- **Solution**: Use more complex model, add features

```
Training Accuracy: 70%
Test Accuracy: 68%  ❌ Both low!
```

### Ideal Fit ✅
```
Training Accuracy: 85%
Test Accuracy: 83%  ✅ Similar and high!
```

---

## Important Terms

### Accuracy
Percentage of correct predictions
```
Accuracy = Correct Predictions / Total Predictions
```

### Model
Algorithm + learned parameters
Transforms features into predictions

### Hyperparameters
Settings you configure before training
Example: `train_test_split(test_size=0.2)`

### Cross-Validation
Multiple train-test splits to better estimate performance

### Bias
Error due to oversimplified model

### Variance
Error due to model being too complex

---

## Data Pipeline

```
Raw Data
    ↓
Data Cleaning (Handle missing values)
    ↓
Feature Engineering (Create/select features)
    ↓
Train-Test Split
    ↓
Model Training (on train set)
    ↓
Model Evaluation (on test set)
    ↓
Prediction/Deployment
```

## Key Takeaway:
Understanding these concepts is crucial for building effective ML models!
        """
    }
}

def get_lesson(lesson_id):
    """Retrieve lesson content"""
    return LESSONS.get(lesson_id)

def get_all_lessons():
    """Get all lessons"""
    return LESSONS