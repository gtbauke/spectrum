# Validation Service Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `ValidationService._calculate_predictions` to support matrix-based expressions (`x[:, i]`, `t[i]`) and use stable Pareto Front IDs for column naming, then synchronize the frontend.

**Architecture:** 
- The backend will use `np.stack` to create a 2D feature matrix `x` and provide the parameter list `t` in the evaluation context.
- Prediction columns will be named `model_{id}`.
- The frontend will transition from index-based lookup to ID-based lookup for validation data.

**Tech Stack:** Python 3.12, FastAPI, NumPy, Pandas, React, TypeScript, ECharts.

---

### Task 1: Backend - ValidationService Rewrite

**Files:**
- Modify: `packages/workers/services/validation_service.py`

- [ ] **Step 1: Update `validate` method**
  - Extract `ids = pareto_df["Id"].tolist()`
  - Pass `ids` to `_calculate_predictions`

- [ ] **Step 2: Rewrite `_calculate_predictions`**
  - Update signature: `def _calculate_predictions(self, model_path: str, dataset_path: str, ids: list[int | str], expressions: list[str], parameters: list[list[float]]) -> pd.DataFrame`
  - Implement strict `"target"` column detection.
  - Create 2D feature matrix `x`.
  - Update `eval_context` with mapping for `x`, `t`, `xi`, `ti`.
  - Use `model_{mid}` as result keys.

- [ ] **Step 3: Verify backend locally**
  - Run the worker in a test environment or perform a dry-run of the calculation logic.

### Task 2: Frontend - ModelInsights Synchronization

**Files:**
- Modify: `packages/frontend/app/components/ui/notebook/sections/models/model-insights.component.tsx`

- [ ] **Step 1: Update selection logic**
  - Update `toggleSelection` to use the `Id` from `pareto_df` instead of the index.

- [ ] **Step 2: Update chart data lookup**
  - In `validationOption` use-memo, lookup predictions using `model_{item.Id}`.

- [ ] **Step 3: Update display labels**
  - Change "UNIT {idx}" to "MODEL #{item.Id}" or similar for consistency.

### Task 3: Verification & Polish

- [ ] **Step 1: End-to-End Test**
  - Capture a new validation run and verify the charts in the frontend.
