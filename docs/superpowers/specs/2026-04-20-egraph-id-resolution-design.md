# Egraph ID Resolution in Inference Results and IQL Design

## Overview
This document specifies the design for mapping Egraph IDs directly to saved inference results and adding first-class support for explicit extraction of these expression nodes. This solves the problem where the backend prediction endpoint previously expected an internal Egraph ID which the frontend did not have access to, and enables IQL to fetch nodes that are not natively selected into the `pareto_front`.

## Architectural Components

### 1. Database and Domain Expansion
- **Domain Object**: Add `egraph_id: str | None = None` to the `InferenceResult` model (`packages/core/core/features/profiles/blocks/inference/inference_result.py`).
- **Database Model**: Add `egraph_id` as an optional string column on the `InferenceResultORM` (`packages/db_core...`).
- **Database Migration**: A new Alembic migration to propagate the `egraph_id` column explicitly to the database.

### 2. IQL Query Executor Engine
- The `QueryExecutor` is responsible for translating backend Rust execution dataframes down into pure python domain objects.
- In `packages/inference_query_language/iql/executor/query_executor.py`, intercept the mapping where `Id` maps generically into domain mapping payloads, assigning the native Rust Egraph `Id` string into the new `egraph_id` property.
- Included within `QueryExecutor` is `_ACCEPTED_WHERE_LITERALS`. Append `"id"` into this tuple so IQL supports filtering via explicit IDs (e.g. `SELECT expression FROM m1 WHERE id = 123`).

### 3. Predict Endpoint Fallback Resolution
- The `POST /api/models/{model_id}/predict` endpoint in `packages/backend/app/features/profiles/models/routers/models.py`.
- **Primary Resolution:** Try to parse `request.expression_id` as a UUID. If it succeeds, bypass `pareto_front` entirely and leverage `uow.inference_results.get_by_id(expr_id)` to extract the expression logic strings directly, regardless of where the node previously scored on the search frontier.
- **Fallback Resolution:** If the `expression_id` is an internal raw string (such as the raw Egraph ID), iterate matching `expr.get("Id")` upon `model.metrics["pareto_front"]` array payloads identical to current behavior. 

## Testing and Verification
- Verifying the creation of Alembic revisions via `alembic upgrade head`.
- Ensure querying natively `WHERE id = 5000` fetches specifically one node payload reliably returning the right prediction results directly inside IQL payload queries dynamically.
