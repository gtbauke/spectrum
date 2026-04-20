# Spectrum Model Predictability Feature Design

## Overview
This document outlines the design for the model predictability feature across the Spectrum stack. The feature allows users to submit feature values ($x_0$, $x_1$, $t_0$, etc.) and instantly predict the dependent variable output of a symbolic regression model's expressions.

## Architectural Components

### 1. External Integration Endpoint (Backend API)
A RESTful dedicated endpoint allowing external clients to fetch inference predictions based on generated expressions of the model.

- **Route:** `POST /api/models/{model_id}/predict`
- **Request Format:** 
  The endpoint accepts an array or map allowing multiple items (rows of predictions) to be tested at once.
  ```json
  {
    "expression_id": "optional-uuid", // if omitted, grabs the top-rated fitness expression of the model
    "inputs": [
      { "x0": 1.5, "x1": 2.0 },
      { "x0": 3.0, "x1": 4.5 }
    ]
  }
  ```
- **Response Format:**
  ```json
  {
    "expression_id": "resolved-uuid",
    "predictions": [3.6, 9.8] // the computed Y values corresponding to the inputs array
  }
  ```
- **Logic:** Calls a shared `PredictionEvaluationService` to securely perform numerical evaluation.

### 2. IQL Engine Integration (Syntax Level)
For direct queries into the Inference Query Language, predictability will be supplied as a modifying clause on the existing `SELECT` node.

- **Syntax:** `SELECT expression, fitness, PREDICT(x0=1.5, x1=2.0) FROM model_name TOP 10`
- **Execution Mechanism:** 
  - Tokenization and syntax parsing will handle `PREDICT(...)` as a column extension inside `SelectClauseAstNode`. 
  - The `QueryExecutor` captures the requested feature payload mappings (e.g. `x0=1.5, x1=2.0`), executes the base expression logic, and injects the mathematical evaluation results dynamically into a new `prediction` field on each mapped `InferenceResult`.

### 3. Shared Evaluation Service (Backend Services)
In `workers/services/validation_service.py`, numpy-based prediction string parsing logic already exists. This logic will be abstracted out into a generalized `PredictionEvaluationService` (e.g. under `packages/core/core/features/profiles/blocks/inference`) ensuring math evaluation logic remains isolated, well-tested, and perfectly DRY across both backend endpoints and the IQL Executor. 

### 4. Direct Client Evaluation (Frontend UI)
Within the frontend editor notebook (`inference-block.component.tsx`), quick variable checking shouldn't require network latency hitting the backend again. 

- **Implementation:** Inside the `ResultItem` component, an expandable "Test Variables" module will parse generic strings like `x0` and `x1` using Regex out of the `numpy` expression block. 
- **UX:** Renders small numeric field layouts for detected variable placeholders. 
- **Compute:** Employs an interactive client-side execution block using `mathjs` to recalculate evaluation dynamically upon input changing natively in the browser. 

## Non-Goals
- We are not updating regression e-graph parameters or initiating fine-tuning; this is strictly numerical application of discovered mathematics.
- The `mathjs` frontend logic does not affect what is serialized into the DB. It remains decoupled from backend `Numpy` environment structures.
