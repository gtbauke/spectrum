# Fix Model Binary Parsing Error (Reggression Library)

Status: Draft
Date: 2026-04-05

## Problem Statement

The user is encountering a Haskell-level binary parsing error (`Data.Binary.Get.runGet at position 3456: not enough bytes`) when initializing the `Reggression` library in the inference worker. This is caused by `RunCreatedHandler` incorrectly storing the path to the `results.csv` file in the `Model.path` field, which the inference engine then attempts to parse as a binary e-graph dump.

## Proposed Changes

### Layer: Application (Workers)

#### [MODIFY] `packages/workers/handlers/run_created.py`

- **Correct Path Mapping**: Update the model creation logic to use `egraph_upload.path` instead of `results_upload.path`.
- **Validation**: Ensure that `result.egraph_dump` is present before attempting to create the `Model` record.
- **Improved Error Handling**: If the e-graph dump is missing from the training result, the run should be marked as `FAILED` with a descriptive error message: "Missing e-graph dump from training results".

### Layer: Domain (Core)

#### [DOC] `packages/core/core/features/profiles/models/model.py`
- Add code documentation to the `path` field of the `Model` entity, explicitly stating it should point to the binary deserialized state (e-graph) used by the regression engine.

## Data Flow & Architecture

1. **Training Completed**: `TrainingService` emits a `TrainingResult` containing `results_csv` and `egraph_dump`.
2. **Post-Processing**: `RunCreatedHandler` uploads both files to localized storage (`profiles/{profile_id}/models/{run_id}/`).
3. **Database Initialization**: A `Model` entity is created, with `path` pointing to `/egraph.dump`.
4. **Inference Execution**: `InferenceRunRequestedHandler` downloads the e-graph file and passes it to `Reggression(loadFrom=path)`.
5. **Success**: Haskell parsing succeeds as the input format (binary) matches the expected e-graph structure.

## Verification Plan

### Automated Tests
- Create a unit test for `RunCreatedHandler` to verify that the `Model` created points to the `.dump` file, not the `.csv` file.
- Verify `setup_logging` and worker startup (as previously addressed) to ensure logs are visible for debugging.

### Manual Verification
- Execute a training job in the notebook UI.
- Execute an inference query against the resulting model.
- Confirm the `InferenceRunRequestedHandler` log shows "Successfully handled message" and produces mathematical expressions in the results pane.
