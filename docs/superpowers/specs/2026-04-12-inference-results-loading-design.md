# Design Spec: Inference Block Results Loading

This document outlines the design for loading the latest inference results together with the profile editor in the Spectrum platform.

## Goal

Ensure that when a user opens a profile in the notebook editor, any previously executed inference blocks automatically display their last results, avoiding the need for re-execution or manual fetching.

## Proposed Changes

### 1. Domain Layer (`packages/core`)

We will update the `InferenceBlock` data model to include fields for the last execution result and status.

#### `packages/core/core/features/profiles/blocks/block_kind.py`

Update `InferenceBlock` to carry the results and execution metadata:

```python
class InferenceBlock(BaseBlock[str]):
    kind: Literal[BlockKind.INFERENCE] = BlockKind.INFERENCE
    results: list[InferenceResult] = Field(default_factory=list)
    status: InferenceRunStatus = Field(default=InferenceRunStatus.PENDING)
    execution_time_ms: Optional[int] = None
    error: Optional[str] = None
```

### 2. Database Layer (`packages/db_core`)

We will update the repository and mapping logic to hydrate these new fields when fetching blocks.

#### `packages/db_core/db/features/profiles/blocks/repository.py`

Update the `SqlAlchemyBlocksRepository` to join with the latest `InferenceRun` and its results when listing or getting blocks for a profile.

- **Join Strategy**: Perform an `LEFT OUTER JOIN` on `inference_runs` where `is_latest=True`.
- **Relationship**: The results will be fetched from the `inference_results` table associated with that run.

#### `packages/db_core/db/features/profiles/blocks/mapper.py`

Update the `BlockMapper` to:
1. Detect if the block is of kind `inference`.
2. Extract the run results from the joined ORM relationship (if any).
3. Populate the `results`, `status`, and `execution_time_ms` fields in the domain `InferenceBlock`.

### 3. Frontend Layer (`packages/frontend`)

#### `packages/frontend/app/utils/types/editor.types.ts`

Update the `InferenceData` type to include the results and status fields returned by the backend.

```typescript
export type InferenceData = {
    code: string;
    results?: InferenceResult[];
    status: InferenceRunStatus;
    executionTimeMs?: number;
    error?: string;
    activeRunId?: string;
};
```

#### `packages/frontend/app/stores/editor.store.ts`

Update `initializeProfileBlocks` to correctly map the backend `Block` data into the frontend `EditorBlock` state:

```typescript
const dynamicBlocks: EditorBlock[] = (profile.blocks || []).map((b) => {
    if (b.kind === "inference") {
        const inferenceData = b.data as any; // Cast to access expanded fields
        return {
            id: b.id,
            type: "inference",
            data: {
                code: inferenceData.data,
                results: inferenceData.results || [],
                status: inferenceData.status || "idle",
                executionTimeMs: inferenceData.execution_time_ms,
                error: inferenceData.error,
            },
        } as EditorBlock;
    }
    // ...
});
```

## Verification Plan

### Automated Tests
- **Integration Test**: Fetch a profile with existing inference runs and verify the returned blocks contain the results.
- **Unit Test (Mapper)**: Verify `BlockMapper` correctly handles blocks with and without latest runs.

### Manual Verification
1. Open a profile in the browser.
2. Run an inference query in a block.
3. Refresh the page or navigate away and back.
4. Verify the results are still visible in the block without re-running.
