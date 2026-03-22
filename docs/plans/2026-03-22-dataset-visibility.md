# Dataset Visibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement public/private visibility for datasets so users can share datasets with others while maintaining ownership control.

**Architecture:** 
- Add `DatasetVisibility` enum (PRIVATE, PUBLIC).
- Add `visibility` field to `Dataset` domain model and `DatasetORM`.
- Use the existing `BaseFilter.OR` capability to allow `list_datasets` to show own datasets + others' public ones.
- Secure `get_dataset` and `delete_dataset` with owner-only or visibility-aware guards.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2.

---

### Task 1: Domain Model Changes

**Files:**
- Modify: `packages/core/core/features/datasets/dataset.py`
- Modify: `packages/core/core/features/datasets/where.py`
- Create: `packages/core/core/features/datasets/visibility.py`

- [ ] **Step 1: Create DatasetVisibility enum**
  Create `packages/core/core/features/datasets/visibility.py` with `DatasetVisibility(StrEnum)` (PRIVATE, PUBLIC).

- [ ] **Step 2: Add visibility to Dataset domain model**
  Modify `packages/core/core/features/datasets/dataset.py` to add `visibility: DatasetVisibility` field defaulting to `PRIVATE`. Update `.new()` factory.

- [ ] **Step 3: Add visibility to DatasetFilter**
  Modify `packages/core/core/features/datasets/where.py` to add `visibility: EnumFilter[DatasetVisibility] | None = None`.

- [ ] **Step 4: Commit domain changes**
  ```bash
  git add packages/core/core/features/datasets/
  git commit -m "feat(domain): add DatasetVisibility enum and field"
  ```

### Task 2: Database Layer Changes

**Files:**
- Modify: `packages/db_core/db/features/datasets/model.py`
- Modify: `packages/db_core/db/features/datasets/mapper.py`

- [ ] **Step 1: Add visibility column to DatasetORM**
  Modify `packages/db_core/db/features/datasets/model.py` to add `visibility: Mapped[DatasetVisibility] = mapped_column(Enum(DatasetVisibility), ...)`

- [ ] **Step 2: Update DatasetsMapper**
  Modify `packages/db_core/db/features/datasets/mapper.py` to include `visibility` in `to_domain` and `to_orm`.

- [ ] **Step 3: Commit DB layer changes**
  ```bash
  git add packages/db_core/db/features/datasets/
  git commit -m "feat(db): add visibility to DatasetORM and mapper"
  ```

### Task 3: API Layer Changes (Listing & Guards)

**Files:**
- Modify: `packages/backend/app/features/datasets/routers/datasets.py`

- [ ] **Step 1: Update list_datasets logic**
  Implement the `OR` logic using `DatasetFilter(OR=[...])` to show your own datasets OR public datasets when `mine=False`.

- [ ] **Step 2: Update get_dataset guard**
  Add logic to `get_dataset` to raise `Forbidden()` if a user tries to access a PRIVATE dataset they don't own.

- [ ] **Step 3: Update upload_dataset**
  Allow passing `visibility` in the upload form.

- [ ] **Step 4: Run basic verification**
  Run `py_compile` on modified files.

- [ ] **Step 5: Commit API changes**
  ```bash
  git add packages/backend/app/features/datasets/
  git commit -m "feat(api): implement visibility filtering and guards"
  ```

### Task 4: Manual Verification

- [ ] **Step 1: Attempt to list datasets**
  Verify you see your private ones and others' public ones.
- [ ] **Step 2: Attempt to get private dataset of another user**
  Verify it returns 404.
- [ ] **Step 3: Attempt to get public dataset of another user**
  Verify it returns 200.
