# Inference Block Results Loading Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Load the latest inference results together with the profile editor so users don't have to re-run queries to see previous results.

**Architecture:** Integrate the latest `InferenceRun` data into the `InferenceBlock` domain model. Hydrate this data in the `BlockMapper` during profile/block retrieval by joining with the `inference_runs` and `inference_results` tables. Update the frontend `EditorStore` to populate state from this enriched block data.

**Tech Stack:** Python 3.12, SQLAlchemy 2.0, FastAPI, Pydantic v2, React, Zustand.

---

### Task 1: Update InferenceBlock Domain Model

**Files:**
- Modify: `packages/core/core/features/profiles/blocks/block_kind.py`

- [ ] **Step 1: Update InferenceBlock class**
Update the `InferenceBlock` class to include `results`, `status`, `execution_time_ms`, and `error`.

```python
from core.features.profiles.blocks.inference.inference_result import InferenceResult
from core.features.profiles.blocks.inference.inference_run import InferenceRunStatus

class InferenceBlock(BaseBlock[str]):
    kind: Literal[BlockKind.INFERENCE] = BlockKind.INFERENCE
    results: list[InferenceResult] = Field(default_factory=list)
    status: InferenceRunStatus = Field(default=InferenceRunStatus.PENDING)
    execution_time_ms: Optional[int] = None
    error: Optional[str] = None
```

- [ ] **Step 2: Commit**
```bash
git add packages/core/core/features/profiles/blocks/block_kind.py
git commit -m "feat(core): add results and status to InferenceBlock domain model"
```

### Task 2: Update Database Models & Relationships

**Files:**
- Modify: `packages/db_core/db/features/profiles/blocks/model.py`
- Modify: `packages/db_core/db/features/profiles/blocks/inference/model.py`

- [ ] **Step 1: Add relationship to BlockORM**
Add a relationship to `InferenceRunORM` in `BlockORM` to facilitate joined loading.

```python
# In packages/db_core/db/features/profiles/blocks/model.py
    inference_runs: Mapped[list["InferenceRunORM"]] = relationship(
        "InferenceRunORM",
        back_populates="block",
        cascade="all, delete-orphan",
        primaryjoin="foreign(InferenceRunORM.block_id) == BlockORM.id"
    )
```

- [ ] **Step 2: Add back_populates to InferenceRunORM**
```python
# In packages/db_core/db/features/profiles/blocks/inference/model.py
    block: Mapped["BlockORM"] = relationship(
        "BlockORM",
        back_populates="inference_runs"
    )
```

- [ ] **Step 3: Commit**
```bash
git add packages/db_core/db/features/profiles/blocks/model.py packages/db_core/db/features/profiles/blocks/inference/model.py
git commit -m "feat(db): add relationship between blocks and inference runs"
```

### Task 3: Update Block Mapper

**Files:**
- Modify: `packages/db_core/db/features/profiles/blocks/mapper.py`

- [ ] **Step 1: Update to_domain to handle inference results**
Modify `to_domain` to check for the latest inference run and populate the `InferenceBlock` fields.

- [ ] **Step 2: Commit**
```bash
git add packages/db_core/db/features/profiles/blocks/mapper.py
git commit -m "feat(db): update BlockMapper to hydrate inference results"
```

### Task 4: Update Repository to use Joined Loading

**Files:**
- Modify: `packages/db_core/db/features/profiles/blocks/repository.py`

- [ ] **Step 1: Update list and get_unique methods**
Ensure that when fetching blocks, we use `selectinload` or `joinedload` for `inference_runs` and their `results`.

- [ ] **Step 2: Commit**
```bash
git add packages/db_core/db/features/profiles/blocks/repository.py
git commit -m "feat(db): use joined loading for inference runs in blocks repository"
```

### Task 5: Frontend Hydration

**Files:**
- Modify: `packages/frontend/app/utils/types/editor.types.ts`
- Modify: `packages/frontend/app/stores/editor.store.ts`

- [ ] **Step 1: Update InferenceData type**
- [ ] **Step 2: Update initializeProfileBlocks logic**
- [ ] **Step 3: Commit**
```bash
git add packages/frontend/app/utils/types/editor.types.ts packages/frontend/app/stores/editor.store.ts
git commit -m "feat(frontend): hydrate inference results in editor store"
```
