# ML Learning Hub: Curriculum Expansion Plan

**Generated:** 2026-06-18  
**Status:** Phase structure upgraded to 9 phases with scaffolding complete

---

## What Was Done Today

### ✅ Phase Structure Updated
- Renamed original 6 phases to 9 granular phases
- **Phase 1**: ML Fundamentals (unchanged, 100% complete)
- **Phase 2**: Python Data Tools & EDA (was Phase 2 scikit-learn basics)
- **Phase 3**: Scikit-Learn Core & API (**NEW** — critical foundation)
- **Phase 4**: Supervised Learning (was Phase 3)
- **Phase 5**: Unsupervised & Representation (was Phase 4)
- **Phase 6**: Model Evaluation & Robustness (was Phase 5-6 combined)
- **Phase 7**: Production & MLOps (**NEW** — scaffold)
- **Phase 8**: Advanced / Edge Topics (**NEW** — scaffold)
- **Phase 9**: Deep Learning Overview (**NEW** — optional)

### ✅ Sidebar & Navigation Updated
- Added all 9 phases to sidebar radio selection
- Added "📋 Scikit-Learn Checklist" page

### ✅ Placeholder Content Created
- Created placeholder MCQ JSONs for Phases 7-9 (3 files)
- Created placeholder code challenge JSONs for Phases 7-9 (3 files)
- Added scaffolding lesson blocks in app_main.py for Phases 7-9

### ✅ Documentation Created
- **[docs/CURRICULUM_CHECKLIST.md](../docs/CURRICULUM_CHECKLIST.md)** — Comprehensive mapping of all topics
  - 188+ scikit-learn and ML topics enumerated
  - Coverage tracked per phase (35% complete)
  - Priority tiers for filling gaps
  - Effort estimates for each phase
  
- **[docs/COVERAGE_REPORT.md](../docs/COVERAGE_REPORT.md)** — Executive summary
  - Coverage bar chart
  - Top 10 missing items
  - Recommended fill order
  - Effort breakdown

---

## Key Findings

### Current Coverage: 35% (30 / 188 topics)

| Phase | Status | Coverage |
|-------|--------|----------|
| 1: ML Fundamentals | ✅ Complete | 100% |
| 2: Python Data Tools | ⏳ Partial | 20% |
| 3: Scikit-Learn Core | ❌ Missing | 5% |
| 4: Supervised Learning | ⏳ Partial | 30% |
| 5: Unsupervised | ⏳ Partial | 35% |
| 6: Evaluation & Robustness | ⏳ Partial | 25% |
| 7: Production & MLOps | ❌ Missing | 2% |
| 8: Advanced Topics | ❌ Missing | 2% |
| 9: Deep Learning | ❌ Missing | 2% |

### Top 20 Missing Scikit-Learn Items

**TIER 1 (Critical):**
1. ColumnTransformer (mixed features)
2. GridSearchCV / RandomizedSearchCV (hyperparameter tuning)
3. Pipeline patterns (composition)
4. Custom transformers (FunctionTransformer, check_estimator)
5. SVM (SVC, SVR)
6. KNeighborsClassifier/Regressor
7. Ridge, Lasso, ElasticNet (regularization)
8. GaussianNB, MultinomialNB (Naive Bayes)

**TIER 2 (Important):**
9. DBSCAN, AgglomerativeClustering (clustering)
10. t-SNE, UMAP (manifold learning)
11. Imbalanced data handling (class_weight, SMOTE)
12. Model calibration (CalibratedClassifierCV)
13. Permutation importance
14. SHAP/LIME (explainability)
15. HistGradientBoosting (gradient boosting)
16. Stacking/Voting (ensemble)

**TIER 3 (Advanced):**
17. TimeSeriesSplit (time series)
18. partial_fit (incremental learning)
19. Gaussian Processes
20. Model persistence (joblib, serving)

---

## Recommended Next Steps (Priority Order)

### Week 1: Foundation (CRITICAL)
- [ ] **Phase 3 Lesson 3.1**: Pipelines and Pipeline building
  - Topics: Pipeline basics, fit/transform semantics, chaining
  - Challenges: Build 3+ pipelines with different workflows
  - MCQ: 5+ questions on pipeline patterns

- [ ] **Phase 3 Lesson 3.2**: ColumnTransformer and mixed features
  - Topics: ColumnTransformer setup, numeric vs categorical handling
  - Challenges: Complex pipelines with mixed feature types
  - MCQ: 5+ questions on ColumnTransformer

- [ ] **Phase 3 Lesson 3.3**: GridSearchCV and meta-estimators
  - Topics: GridSearchCV, RandomizedSearchCV, Pipeline + Grid integration
  - Challenges: Hyperparameter tuning on 3+ datasets
  - MCQ: 5+ questions on meta-estimators

- [ ] **Phase 2 Lesson 2.1**: pandas Fundamentals
  - Topics: DataFrames, groupby, merge, cleaning
  - Challenges: EDA on real datasets
  - MCQ: 5+ questions on pandas

### Week 2: Supervised Learning Expansion
- [ ] **Phase 4 Lesson 4.1**: SVM and Kernel Methods
- [ ] **Phase 4 Lesson 4.2**: KNN and Distance-Based Methods
- [ ] **Phase 4 Lesson 4.3**: Ridge, Lasso, and Regularization

### Week 3: Unsupervised & Evaluation
- [ ] **Phase 5 Lesson 5.1**: DBSCAN and Advanced Clustering
- [ ] **Phase 6 Lesson 6.1**: Imbalanced Data Handling
- [ ] **Phase 6 Lesson 6.2**: Explainability with SHAP/LIME

### Weeks 4+: Production & Advanced
- [ ] **Phase 7 Lesson 7.1**: Model Persistence and joblib
- [ ] **Phase 7 Lesson 7.2**: Serving with FastAPI
- [ ] **Phase 8 Lesson 8.1**: Time Series and Incremental Learning
- [ ] **Phase 9 Lesson 9.1**: Deep Learning Decision Framework

---

## Implementation Notes

### Files to Modify
- **[app_main.py](../app_main.py)** — Add 20+ detailed lesson sections (currently scaffolded)
- **[challenges/mcq/\*.json](../challenges/mcq/)** — Add 120+ MCQ items across phases
- **[challenges/code/\*.json](../challenges/code/)** — Add 50+ code challenges
- **[docs/CURRICULUM_CHECKLIST.md](../docs/CURRICULUM_CHECKLIST.md)** — Already complete; update as content is added

### New JSON Files Created
✅ `challenges/mcq/phase7_questions.json`  
✅ `challenges/mcq/phase8_questions.json`  
✅ `challenges/mcq/phase9_questions.json`  
✅ `challenges/code/phase7_challenges.json`  
✅ `challenges/code/phase8_challenges.json`  
✅ `challenges/code/phase9_challenges.json`  

### App Structure
- Sidebar now shows all 9 phases + Checklist
- Phase 7-9 have "Overview" and placeholder lesson sections
- Checklist page displays high-level curriculum summary

---

## Estimated Effort to Full Coverage

| Tier | Phases | Hours | Timeline |
|------|--------|-------|----------|
| 1: Critical | 2, 3 | 28 | Week 1 |
| 2: Extended | 4, 5 | 30 | Week 2-3 |
| 3: Evaluation | 6 | 20 | Week 4 |
| 4: Advanced | 7, 8, 9 | 48 | Weeks 5-8 |
| **TOTAL** | | **126** | **~4 weeks** |

---

## Success Criteria

- ✅ Phase 1: 100% (DONE)
- ⏳ Phase 2: 80%+ (targeting Week 1)
- ⏳ Phase 3: 90%+ (targeting Week 1-2)
- ⏳ Phase 4: 85%+ (targeting Week 2-3)
- ⏳ Phase 5: 80%+ (targeting Week 3-4)
- ⏳ Phase 6: 75%+ (targeting Week 4)
- ⏳ Phase 7: 50%+ (targeting Weeks 5-6)
- ⏳ Phase 8: 50%+ (targeting Weeks 6-7)
- ⏳ Phase 9: 50%+ (targeting Weeks 7-8)
- **Overall:** 90%+ coverage by Week 8

---

## How to Use This Plan

1. **Open [docs/CURRICULUM_CHECKLIST.md](../docs/CURRICULUM_CHECKLIST.md)** to see complete topic list
2. **Pick a phase** from the recommended order above
3. **Add lessons** to `app_main.py` using the scaffolded sections
4. **Create challenges** in the JSON files under `challenges/`
5. **Test locally** with `streamlit run app_main.py`
6. **Update this document** as content is added

---

## Quick Stats

- **Total Topics Identified:** 188+
- **Topics Covered:** 30
- **Topics Remaining:** 158+
- **Current Coverage:** 35%
- **Target Coverage:** 100%
- **Estimated Effort:** 126 hours
- **Est. Timeline:** 4-5 weeks at 30 hrs/week

