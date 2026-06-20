"""
Phase 2: Scikit-Learn Basics
"""

LESSONS = {
    "2.1": {
        "title": "Scikit-Learn Core Concepts",
        "duration": "45 minutes",
        "content": """
# 2.1: Scikit-Learn Core Concepts

## What is scikit-learn?
scikit-learn is the most popular Python library for machine learning.
It provides a consistent API for:
- classification
- regression
- clustering
- preprocessing
- model selection

## Estimator pattern
A typical estimator supports:
- `fit(X, y)` → learn from data
- `predict(X_new)` → make predictions
- `score(X, y)` → evaluate performance

## Example
```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()
X, y = iris.data, iris.target

model = DecisionTreeClassifier()
model.fit(X, y)
print(model.score(X, y))
```

## Key ideas
- `X` = features
- `y` = target labels
- `fit` trains the model
- `predict` returns model predictions
- `score` computes accuracy
"""
    },
    "2.2": {
        "title": "Data Preprocessing",
        "duration": "60 minutes",
        "content": """
# 2.2: Data Preprocessing

## Why preprocessing matters
Many models work better when:
- features are scaled
- categories are encoded
- missing values are handled

## Common transformers
- `StandardScaler()` → mean 0, variance 1
- `MinMaxScaler()` → range [0, 1]
- `OneHotEncoder()` → convert categories to binary columns
- `OrdinalEncoder()` → convert categories to integers

## Pipeline
Use `Pipeline` to combine preprocessing + model:
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=200))
])

pipe.fit(X_train, y_train)
```

## Benefits
- cleaner code
- reusable workflow
- less risk of leaking test information
"""
    },
    "2.3": {
        "title": "Model Selection & Validation",
        "duration": "60 minutes",
        "content": """
# 2.3: Model Selection & Validation

## Train-test split
Split data before training:
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

## Cross-validation
Better than one split:
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
print(scores)
```

## Hyperparameter tuning
Find best settings with `GridSearchCV`:
```python
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

param_grid = {'max_depth': [1, 2, 3, 4, 5]}
search = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=3)
search.fit(X, y)
print(search.best_params_)
```

## Key idea
Validation helps you choose the best model and avoid overfitting.
"""
    }
}

def get_lesson(lesson_id):
    return LESSONS.get(lesson_id)

def get_all_lessons():
    return LESSONS