# Platform Integration: IQL Compiler Refactor

This document outlines the changes required in the Spectrum platform (Backend and Worker) to integrate the new modular IQL execution pipeline.

## 1. IQL Worker Integration

### Task Coordination
The IQL Worker currently executes queries as part of inference jobs. 
- **Current Flow**: Receives query string -> Tokenizer -> Parser -> QueryExecutor.
- **New Flow**:
    1. Call `iql.compiler.compile(query)` to obtain the `LogicalPlan`.
    2. (Optional) Check the plan for safety or resource constraints.
    3. Call `iql.executor.execute(plan, regression)` to get the results.
    4. Save the results and the serialized `LogicalPlan` (for provenance) to the database.

### Worker Dependencies
The worker will need to be updated to ensure it can handle the new `IqlErrorCollector` and report more granular errors back to the task coordinator.

## 2. Backend Orchestration

### New Endpoints
To leverage the "transparency" of the new architecture, the backend should implement:
- `GET /inference/validate-query?q=...`: Runs the Tokenizer, Parser, and Analyzer. Returns errors if any. This allows the frontend to show "Red Squiggles" or validation errors in real-time.
- `GET /inference/explain-query?q=...`: Returns the serialized `LogicalPlan` (JSON). This can be used by the frontend to render a visual query plan.

### Inference Feature Updates
The `InferenceService` in `packages/backend/app/features/profiles/blocks/inference/inference_service.py` should be updated to use the new compiler phases when initiating or displaying inference tasks.

## 3. Database Changes
If we want to store the `LogicalPlan` for every executed query:
- Add a `logical_plan` JSONB column to the `InferenceResult` or `InferenceBlock` ORM models.

## 4. Frontend Integration
- **Logical Plan Viewer**: Create a new React component using a graph library (e.g., React Flow) to render the `LogicalPlan` JSON.
- **Real-time Validation**: Integrate the new validation endpoint with the IQL editor to provide immediate feedback.
