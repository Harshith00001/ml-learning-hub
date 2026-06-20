# Phase 4 Expansion Plan: Supervised Learning

**Status:** Ready to Begin  
**Estimated Effort:** 8-10 hours  
**Target XP:** 2,925 XP (matching Phases 2 & 3)

---

## 📋 Phase 4 Overview

**Title:** Supervised Learning — Regression, Classification & Ensembles

**Objective:** Master core supervised learning models with real-world applications

### What to Cover

#### Lesson 4.1: Regression Models (~250 lines)
1. **Linear Regression**
   - Ordinary Least Squares (OLS)
   - Interpreting coefficients
   - R² and residuals

2. **Polynomial & Non-linear Regression**
   - Polynomial features
   - When to use polynomial
   - Avoiding overfitting

3. **Regularized Regression**
   - Ridge (L2) regression
   - Lasso (L1) regression
   - ElasticNet (L1+L2)
   - Alpha/lambda tuning

**Code Examples Needed:**
- Linear regression on house prices
- Polynomial fit on synthetic data
- Ridge vs Lasso comparison
- Cross-validation for alpha selection

**Quiz Ideas:**
- R² interpretation
- Overfitting vs underfitting
- When to use regularization
- Intercept significance

**Code Challenges:**
- Build linear regression model
- Ridge vs Lasso performance
- Hyperparameter tuning
- Residual analysis

---

#### Lesson 4.2: Classification Models (~250 lines)
1. **Logistic Regression**
   - Binary classification
   - Multi-class (softmax)
   - Probability output

2. **Decision Trees & Random Forests**
   - Tree structure
   - Feature importance
   - Ensemble voting

3. **Support Vector Machines (SVM)**
   - Kernel trick
   - C parameter tuning
   - Multi-class strategies

**Code Examples Needed:**
- Binary classification (fraud detection)
- Multi-class classification (iris)
- Random Forest feature importance
- SVM with different kernels

**Quiz Ideas:**
- Tree depth and overfitting
- Feature importance interpretation
- SVM kernel selection
- Ensemble voting strategies

**Code Challenges:**
- Implement logistic regression
- Random Forest classifier
- SVM with grid search
- Feature importance analysis

---

#### Lesson 4.3: Evaluation & Ensemble Methods (~250 lines)
1. **Classification Metrics**
   - Accuracy, Precision, Recall, F1
   - Confusion matrix
   - ROC curve & AUC
   - Precision-Recall curve

2. **Ensemble Methods**
   - Voting classifiers
   - Bagging (Bootstrap Aggregating)
   - Boosting (Gradient Boost, XGBoost)
   - Stacking

3. **Imbalanced Data**
   - Class weights
   - SMOTE
   - Threshold tuning

**Code Examples Needed:**
- Confusion matrix visualization
- ROC curve comparison
- Voting classifier ensemble
- Gradient Boost model
- SMOTE for imbalanced data

**Quiz Ideas:**
- Precision vs Recall trade-off
- ROC AUC interpretation
- Boosting vs Bagging
- When to use each ensemble method

**Code Challenges:**
- ROC curve plotting
- Voting ensemble
- Gradient Boost tuning
- Imbalanced data handling

---

## 🎯 Content Targets

### Quiz Questions (15 total)
**Easy (3):**
- Linear regression basics
- Classification model types
- Ensemble method names

**Medium (8):**
- R², MSE, MAE interpretation
- Precision/Recall trade-off
- Feature importance
- Regularization effects
- Cross-validation strategy

**Hard (4):**
- ROC AUC interpretation
- Boosting vs Bagging tradeoffs
- Imbalanced data strategies
- Multi-metric optimization

### Code Challenges (10 total)
**Easy (2):**
- Basic linear regression
- Logistic regression binary classification

**Medium (6):**
- Ridge vs Lasso comparison
- Random Forest with grid search
- SVM kernel comparison
- Classification metrics
- Feature importance visualization
- Cross-validation with CV score

**Hard (2):**
- Ensemble voting classifier
- Imbalanced data (SMOTE + classification)

---

## 📊 XP Distribution Plan

| Item | Type | Difficulty | XP |
|------|------|-----------|-----|
| L4.1 Regression | Lesson | - | 200 |
| L4.2 Classification | Lesson | - | 200 |
| L4.3 Ensembles | Lesson | - | 200 |
| Q1-3 | Quiz | Easy | 150 |
| Q4-11 | Quiz | Medium | 600 |
| Q12-15 | Quiz | Hard | 400 |
| C1-2 | Challenge | Easy | 175 |
| C3-8 | Challenge | Medium | 600 |
| C9-10 | Challenge | Hard | 350 |
| **TOTAL** | | | **2,875** |

---

## 📝 Implementation Checklist

### Step 1: Update app_main.py
- [ ] Find current Phase 4 placeholder section
- [ ] Replace with Lesson 4.1: Regression (~250 lines)
- [ ] Add Lesson 4.2: Classification (~250 lines)
- [ ] Add Lesson 4.3: Ensembles (~250 lines)
- [ ] Update Quiz section to load phase4_questions.json
- [ ] Update Code Challenges section to load phase4_challenges.json

### Step 2: Create phase4_questions.json
- [ ] 3 easy questions (50 XP each)
- [ ] 8 medium questions (75 XP each)
- [ ] 4 hard questions (100 XP each)
- [ ] Validate JSON syntax

### Step 3: Create phase4_challenges.json
- [ ] 2 easy challenges (75-100 XP each)
- [ ] 6 medium challenges (100-125 XP each)
- [ ] 2 hard challenges (150-200 XP each)
- [ ] Validate JSON syntax

### Step 4: Testing
- [ ] Syntax check (py_compile)
- [ ] JSON validation (json.load)
- [ ] Run all code examples
- [ ] Verify quiz questions load

---

## 🔗 Integration with Existing Content

**Builds on:**
- Phase 1: ML fundamentals
- Phase 2: pandas, NumPy, data preparation
- Phase 3: pipelines, ColumnTransformer, GridSearchCV

**Leads to:**
- Phase 5: Unsupervised learning
- Phase 6: Model evaluation & robustness
- Phase 7: Production & MLOps

---

## 💡 Teaching Notes

### Key Concepts to Emphasize
1. **Regression vs Classification:** When to use each
2. **Metrics Matter:** Different metrics for different problems
3. **Ensemble Power:** Why combining models works
4. **Data Balance:** Handling imbalanced classes
5. **Hyperparameter Tuning:** Systematic vs grid search

### Common Student Mistakes
- Using accuracy on imbalanced data
- Not interpreting feature importance correctly
- Over-tuning on validation set
- Not considering business context for metrics
- Choosing models without cross-validation

### Real-world Examples
- House price prediction (regression)
- Fraud detection (classification, imbalanced)
- Customer churn prediction (binary classification)
- Multi-class sentiment analysis
- Disease diagnosis (medical ML)

---

## 📚 Code Example Structure

### Each Lesson Should Include
1. **Problem statement** (what are we solving?)
2. **Data loading** (use Iris, Titanic, or synthetic)
3. **Model training** (fit the model)
4. **Evaluation** (metrics, visualization)
5. **Interpretation** (what does this mean?)
6. **Best practices** (how to use in production)

### Consistent Code Style
```python
# Imports
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Load & prepare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create & fit
model = SomeModel(parameter=value)
model.fit(X_train, y_train)

# Evaluate
score = model.score(X_test, y_test)
print(f"Score: {score}")
```

---

## 🎓 Expected Learning Outcomes

After Phase 4, students should:
- ✅ Understand regression vs classification
- ✅ Build and train multiple model types
- ✅ Evaluate models with appropriate metrics
- ✅ Handle imbalanced data
- ✅ Use ensemble methods
- ✅ Tune hyperparameters systematically
- ✅ Interpret model results
- ✅ Choose appropriate models for tasks

---

## 📊 Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| Plan outline | ✅ | Complete |
| Content structure | ✅ | 3 lessons defined |
| Quiz topics | ✅ | 15 questions planned |
| Challenge ideas | ✅ | 10 challenges outlined |
| XP distribution | ✅ | 2,875 XP allocated |
| Implementation | ⏳ | Ready to start |
| Testing | ⏳ | Validation planned |
| Deployment | ⏳ | Post-validation |

---

## ⏱️ Timeline Estimate

- **Content Creation:** 4-5 hours (lessons + examples)
- **Quiz Development:** 1-2 hours (15 questions)
- **Challenge Coding:** 1-2 hours (10 challenges)
- **Testing & Validation:** 1 hour
- **Total:** 8-10 hours

---

## 🚀 Ready to Proceed

All planning complete. Phase 4 ready for implementation.

**Next Action:** Start with Lesson 4.1 (Regression)

---

Generated: 2026-06-19
