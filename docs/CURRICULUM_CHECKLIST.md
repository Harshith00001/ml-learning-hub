# Scikit-Learn & Machine Learning Curriculum Checklist

**Last Updated:** 2026-06-18  
**Curriculum Status:** ~35% Complete (30 out of ~180 topics)

---

## Overview

This checklist maps the complete ML Learning Hub curriculum against scikit-learn APIs and core machine learning concepts. It tracks which estimators, transformers, utilities, and topics are covered in lessons and challenges, and identifies gaps for incremental expansion.

---

## PHASE 1: ML Fundamentals
**Status:** ✅ **Complete** | 6 MCQ items | 3 Lessons

### Topics Covered
- ✅ What is Machine Learning
- ✅ Types of ML (Supervised, Unsupervised, Reinforcement)
- ✅ Key Concepts (features, targets, overfitting, train-test split)
- ✅ Terminology and workflow

### Notes
Foundational phase is complete and comprehensive.

---

## PHASE 2: Python Data Tools & EDA
**Status:** ⏳ **Partially Complete** | 6 MCQ items | 3 Lessons

### Covered
- ✅ fit-predict pattern
- ✅ StandardScaler, OneHotEncoder
- ✅ train_test_split
- ✅ GridSearchCV basics

### Missing/Needs Expansion
- ❌ **pandas**: DataFrame operations, groupby, merge, pivoting, cleaning
- ❌ **numpy**: arrays, reshaping, broadcasting, aggregations
- ❌ **Visualization**: matplotlib, seaborn patterns
- ❌ **EDA Workflows**: missing values, outlier detection, distributions
- ❌ **Data Quality**: missing data patterns, class imbalance

**Gap Count:** 5+ major topics  
**Priority:** HIGH (foundation for all other phases)

---

## PHASE 3: Scikit-Learn Core & API
**Status:** ❌ **Not Started** | 0 MCQ items | 0 Lessons

### Critical Missing Topics

#### Estimators & Transformers API (10+ items)
- ❌ `.fit()`, `.transform()`, `.fit_transform()` semantics
- ❌ `.predict()`, `.score()` with examples
- ❌ `.decision_function()` vs `.predict_proba()`
- ❌ `.coef_` and `.feature_importances_` inspection
- ❌ `.get_params()`, `.set_params()`, cloning
- ❌ Transformer vs Predictor contracts

#### Core Transformers (8+ items)
- ❌ StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer
- ❌ OneHotEncoder, OrdinalEncoder, TargetEncoder
- ❌ PolynomialFeatures, FunctionTransformer
- ❌ SimpleImputer, KNNImputer, IterativeImputer
- ❌ SelectKBest, SelectPercentile, RFE

#### Pipelines & Composition (6+ items)
- ❌ Pipeline building and chaining
- ❌ ColumnTransformer for mixed feature types
- ❌ FeatureUnion for feature combination
- ❌ make_pipeline, make_column_selector
- ❌ Complex pipeline patterns and debugging

#### Meta-Estimators (6+ items)
- ❌ GridSearchCV deep dive
- ❌ RandomizedSearchCV
- ❌ Pipeline + GridSearch integration
- ❌ Cross-validation strategies (StratifiedKFold, TimeSeriesSplit)
- ❌ cross_val_score, cross_validate
- ❌ Learning curves for diagnostics

#### Custom Estimators (4+ items)
- ❌ Extending BaseEstimator and TransformerMixin
- ❌ FunctionTransformer for custom transformations
- ❌ check_estimator for validation
- ❌ Best practices and common pitfalls

#### Advanced Utilities (4+ items)
- ❌ get_feature_names_out (sklearn 1.0+)
- ❌ clone() for copying estimators
- ❌ set_config for pandas output
- ❌ get_feature_names patterns

**Gap Count:** 38+ major subtopics (CRITICAL)  
**Priority:** HIGHEST (foundation for all downstream phases)

---

## PHASE 4: Supervised Learning
**Status:** ⏳ **Partially Complete** | 5 MCQ items | 3 Lessons | 3 Code Challenges

### Covered
- ✅ LinearRegression, LogisticRegression (basic)
- ✅ DecisionTreeClassifier/Regressor
- ✅ RandomForestClassifier/Regressor

### Missing/Needs Expansion

#### Linear & Regularized Models (8 items)
- ❌ Ridge, Lasso, ElasticNet (L1/L2 regularization)
- ❌ SGDRegressor, SGDClassifier (incremental)
- ❌ LinearSVR, LinearSVC
- ❌ HuberRegressor, QuantileRegressor
- ❌ PassiveAggressive models
- ❌ Logistic regression with class weights

#### SVM & Distance-Based (4 items)
- ❌ SVC, SVR (RBF, polynomial kernels)
- ❌ NuSVC, NuSVR
- ❌ OneClassSVM
- ❌ Kernel tricks and parameter tuning

#### KNN & Naive Bayes (4 items)
- ❌ KNeighborsClassifier/Regressor
- ❌ RadiusNeighborsClassifier/Regressor
- ❌ GaussianNB, MultinomialNB, BernoulliNB
- ❌ ComplementNB

#### Tree & Ensemble Variants (6 items)
- ❌ ExtraTreesClassifier/Regressor
- ❌ HistGradientBoostingClassifier/Regressor
- ❌ StackingClassifier, StackingRegressor
- ❌ VotingClassifier, VotingRegressor
- ❌ AdaBoostClassifier/Regressor
- ❌ BaggingClassifier/Regressor

#### Feature Engineering (4 items)
- ❌ Feature selection (SelectKBest, RFE, RFECV)
- ❌ Feature interaction patterns
- ❌ Feature scaling best practices
- ❌ Permutation importance

**Gap Count:** 20+ missing estimators and techniques  
**Priority:** HIGH

---

## PHASE 5: Unsupervised & Representation Learning
**Status:** ⏳ **Partially Complete** | 4 MCQ items | 3 Lessons

### Covered
- ✅ KMeans clustering
- ✅ PCA dimensionality reduction
- ✅ IsolationForest anomaly detection

### Missing/Needs Expansion

#### Clustering Methods (8 items)
- ❌ DBSCAN, OPTICS (density-based)
- ❌ AgglomerativeClustering (hierarchical)
- ❌ Birch (incremental)
- ❌ MiniBatchKMeans (out-of-core)
- ❌ SpectralClustering
- ❌ Clustering metrics: silhouette, davies_bouldin, calinski_harabasz
- ❌ Cluster validation and evaluation

#### Dimensionality Reduction (8 items)
- ❌ t-SNE (manifold)
- ❌ UMAP (not in sklearn, but commonly paired)
- ❌ Isomap, LocallyLinearEmbedding
- ❌ TruncatedSVD, FactorAnalysis
- ❌ DictionaryLearning
- ❌ NMF (Non-Negative Matrix Factorization)
- ❌ Manifold method comparison

#### Anomaly Detection Variants (4 items)
- ❌ LocalOutlierFactor
- ❌ EllipticEnvelope
- ❌ OneClassSVM
- ❌ Anomaly detection metrics

#### Feature Extraction (3 items)
- ❌ CountVectorizer, TfidfVectorizer (text)
- ❌ DictVectorizer
- ❌ FeatureHasher

**Gap Count:** 23+ clustering/manifold/extraction methods  
**Priority:** MEDIUM-HIGH

---

## PHASE 6: Model Evaluation & Robustness
**Status:** ⏳ **Partially Complete** | 3 MCQ items | 3 Lessons

### Covered
- ✅ Accuracy, Precision, Recall, F1
- ✅ Confusion Matrix
- ✅ ROC AUC, Cross-Validation basics

### Missing/Needs Expansion

#### Classification Metrics (6 items)
- ❌ PR AUC (Precision-Recall)
- ❌ Matthews Correlation Coefficient
- ❌ Cohen's kappa
- ❌ Balanced accuracy
- ❌ Adjusted mutual information
- ❌ Completeness, homogeneity, v-measure

#### Regression Metrics (5 items)
- ❌ MAE, MSE, RMSE
- ❌ R² score
- ❌ Median absolute error, MAPE
- ❌ Max error
- ❌ Pinball loss

#### Imbalanced Data (6 items)
- ❌ Class weights setup
- ❌ SMOTE oversampling
- ❌ Stratified sampling patterns
- ❌ Threshold optimization
- ❌ Cost-sensitive learning
- ❌ Sampling strategies comparison

#### Model Calibration (4 items)
- ❌ Calibration curves and ECE
- ❌ CalibratedClassifierCV
- ❌ Platt scaling, Isotonic regression
- ❌ Probability output reliability

#### Inspection & Diagnostics (8 items)
- ❌ Permutation importance
- ❌ Learning curves for overfitting/underfitting
- ❌ Partial dependence plots
- ❌ SHAP values and integration
- ❌ LIME explanations
- ❌ Feature importance comparison
- ❌ Decision boundaries visualization
- ❌ Tree model visualization

**Gap Count:** 29+ evaluation and diagnostic methods  
**Priority:** HIGH

---

## PHASE 7: Production & MLOps
**Status:** ✅ COMPLETE

### Completed Phase 7 Content
- Lessons: 3 (Model Persistence & Serving, Containerization & Deployment, Monitoring, Drift & CI/CD)
- Quiz: 15 questions
- Challenges: 10 code problems
- Total XP: 3,275
- Total Items: 28

### Phase 7 Coverage
Phase 7 content is fully implemented in `app_main.py`, validated with `validate_phase7.py`, and wired to the learning dashboard.

---

## PHASE 8: Advanced / Edge Topics
**Status:** ⚠️ **Partial Implementation** | 3 Lessons | 6 MCQ | 3 Challenges

### Critical Missing Topics

#### Time Series (5 items)
- ❌ TimeSeriesSplit for cross-validation
- ❌ Lag features and rolling statistics
- ❌ Trend and seasonality handling
- ❌ Autoregressive patterns
- ❌ Temporal feature engineering

#### Incremental & Out-of-Core (5 items)
- ❌ partial_fit() for SGDClassifier/Regressor
- ❌ MiniBatchKMeans, IncrementalPCA
- ❌ Online learning workflows
- ❌ Streaming data patterns
- ❌ Memory-efficient pipelines

#### Custom Estimators (4 items)
- ❌ Custom estimator creation patterns
- ❌ check_estimator for validation
- ❌ Mixin classes and inheritance
- ❌ Base class contracts

#### Probabilistic & Bayesian (4 items)
- ❌ Gaussian Processes (GaussianProcessClassifier/Regressor)
- ❌ Bayesian Ridge Regression
- ❌ Uncertainty quantification
- ❌ Confidence intervals

#### Explainability (5 items)
- ❌ SHAP integration and usage
- ❌ LIME for local explanations
- ❌ Permutation importance deep dive
- ❌ Partial dependence advanced patterns
- ❌ Tree model interpretation

**Gap Count:** 23+ advanced topics  
**Priority:** MEDIUM-LOW

---

## PHASE 9: Deep Learning Overview
**Status:** ⚠️ **Partial Implementation** | 3 Lessons | 6 MCQ | 3 Challenges

### Critical Missing Topics

#### Decision Framework (3 items)
- ❌ When to use DL vs scikit-learn
- ❌ Use case matrix and trade-offs
- ❌ Cost-benefit analysis

#### TensorFlow/Keras (5 items)
- ❌ Keras Sequential API
- ❌ Custom layers and models
- ❌ Functional API
- ❌ Training loops and callbacks
- ❌ Regularization and dropout

#### PyTorch (5 items)
- ❌ Tensor operations and autograd
- ❌ nn.Module and nn.Functional
- ❌ Custom models and layers
- ❌ Training loops
- ❌ DataLoader and samplers

#### Transfer Learning (4 items)
- ❌ Pre-trained models (ImageNet, BERT)
- ❌ Fine-tuning workflows
- ❌ Domain adaptation
- ❌ Feature extraction reuse

#### Architecture Patterns (2 items)
- ❌ CNNs for images
- ❌ RNNs/Transformers for sequences

**Gap Count:** 19+ DL topics  
**Priority:** LOW (optional advanced track)

---

## Summary Table

| Phase | Name | Topics | Lessons | MCQ | Challenges | Coverage | Gap |
|-------|------|--------|---------|-----|------------|----------|-----|
| 1 | ML Fundamentals | 4 | 3 | 6 | 3+ | 100% | 0% |
| 2 | Python Data Tools & EDA | 5 | 3 | 6 | 3+ | 20% | 80% |
| 3 | Scikit-Learn Core & API | 40+ | 0 | 0 | 0 | 5% | 95% |
| 4 | Supervised Learning | 22+ | 3 | 5 | 3 | 30% | 70% |
| 5 | Unsupervised & Representation | 23+ | 3 | 4 | 2+ | 35% | 65% |
| 6 | Model Evaluation & Robustness | 29+ | 3 | 3 | 2+ | 25% | 75% |
| 7 | Production & MLOps | 28 | 3 | 15 | 10 | 100% | 0% |
| 8 | Advanced / Edge Topics | 23+ | 0 | 1 | 0 | 2% | 98% |
| 9 | Deep Learning Overview | 19+ | 0 | 1 | 0 | 2% | 98% |
| **TOTAL** | | **188+** | **15** | **27** | **13+** | **35%** | **65%** |

---

## Recommended Fill Order (Priority Tiers)

### **TIER 1: Critical Foundation** (Do First)
1. **Phase 3: Scikit-Learn Core & API** (38+ items)
   - Pipelines, ColumnTransformer, GridSearchCV, custom transformers
   - **Est. effort:** 20 hours | **Impact:** VERY HIGH

2. **Phase 2: Python Data Tools & EDA** (5+ items)
   - pandas, numpy, matplotlib, EDA workflows
   - **Est. effort:** 8 hours | **Impact:** HIGH

### **TIER 2: Extended Algorithms** (Next)
3. **Phase 4: Supervised Learning** (20+ items)
   - SVM, KNN, GaussianNB, Ridge/Lasso, Boosting, Stacking
   - **Est. effort:** 15 hours | **Impact:** HIGH

4. **Phase 5: Unsupervised & Representation** (23+ items)
   - DBSCAN, t-SNE, manifold methods, feature extraction
   - **Est. effort:** 15 hours | **Impact:** MEDIUM-HIGH

### **TIER 3: Evaluation & Robustness** (Then)
5. **Phase 6: Model Evaluation & Robustness** (29+ items)
   - Imbalanced data, calibration, explainability (SHAP/LIME)
   - **Est. effort:** 18 hours | **Impact:** MEDIUM

### **TIER 4: Production & Advanced** (Finally)
6. **Phase 7: Production & MLOps** (23+ items)
   - Persistence, serving, MLflow, monitoring
   - **Est. effort:** 18 hours | **Impact:** MEDIUM

7. **Phase 8: Advanced / Edge Topics** (23+ items)
   - Time series, incremental learning, Bayesian, explainability deep dive
   - **Est. effort:** 15 hours | **Impact:** MEDIUM

8. **Phase 9: Deep Learning Overview** (19+ items)
   - When to use DL, TensorFlow/PyTorch primer, transfer learning
   - **Est. effort:** 15 hours | **Impact:** LOW-MEDIUM

---

## Total Effort Estimate

| Tier | Phases | Lessons | MCQ | Challenges | Total Hours |
|------|--------|---------|-----|------------|-------------|
| 1 | 2, 3 | 15 | 30 | 15 | 28 |
| 2 | 4, 5 | 16 | 40 | 20 | 30 |
| 3 | 6 | 10 | 30 | 15 | 20 |
| 4 | 7, 8, 9 | 20 | 40 | 20 | 48 |
| **Total** | | **61** | **140** | **70** | **126 hours** |

**Estimated time to 90% coverage:** ~126 hours (~3 weeks at 30 hrs/week)

---

## Next Steps

1. **Week 1**: Expand Phase 3 (pipelines, ColumnTransformer) + Phase 2 (pandas/numpy)
2. **Week 2**: Expand Phase 4 (SVM, KNN, Ridge/Lasso) + start Phase 5 (DBSCAN, t-SNE)
3. **Week 3**: Expand Phase 6 (imbalanced, calibration, explainability)
4. **Weeks 4+**: Phases 7-9 content and integration

