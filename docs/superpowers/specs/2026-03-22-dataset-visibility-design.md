# Dataset Visibility

**Date:** 2026-03-22
**Status:** Approved

## Summary

Add a `visibility` property to datasets, allowing them to be either **public** or **private**. Public datasets are discoverable and usable by any authenticated user. Private datasets are only visible to their owner. The owner always retains sole write/delete control regardless of visibility.

## Requirements

- Datasets default to **private** on creation
- Owner can toggle visibility between `PRIVATE` and `PUBLIC`
- **Listing**: users see their own datasets (all visibilities) + other users' public datasets
- **Read access**: anyone can read a public dataset; only the owner can read a private one
- **Write/delete access**: always restricted to the owner (unchanged)
- Design should accommodate future enum extensions (e.g., `TEAM`, `SHARED`) without refactoring

## Design

### Domain Layer (`packages/core`)

**New** `DatasetVisibility` enum:

```python
class DatasetVisibility(StrEnum):
    PRIVATE = "private"
    PUBLIC = "public"
```

**Modified** `Dataset` — add field:

```python
visibility: DatasetVisibility = Field(
    DatasetVisibility.PRIVATE,
    description="Controls who can see and use this dataset",
)
```

`Dataset.new()` factory defaults to `PRIVATE`.

**Modified** `DatasetFilter` — add filter:

```python
visibility: EnumFilter[DatasetVisibility] | None = None
```

### Database Layer (`packages/db_core`)

**Modified** `DatasetORM` — add column using existing `Enum()` pattern:

```python
visibility: Mapped[str] = mapped_column(
    Enum(DatasetVisibility), nullable=False, default=DatasetVisibility.PRIVATE,
)
```

**Modified** `DatasetMapper` — map `visibility` between domain enum and ORM column.

**Migration** — `ALTER TABLE datasets ADD COLUMN visibility datasetvisibility NOT NULL DEFAULT 'private'`. Backfills all existing rows as private.

### API Layer (`packages/backend`)

**Modified** `list_datasets` — uses existing `BaseFilter.OR` support:

```python
# Default: own datasets (all visibilities) + others' public
dataset_filter = DatasetFilter(
    OR=[
        DatasetFilter(owner_id=UUIDFilter(eq=current_user_id)),
        DatasetFilter(visibility=EnumFilter(eq=DatasetVisibility.PUBLIC)),
    ]
)

# mine=True: only own datasets
if mine:
    dataset_filter = DatasetFilter(owner_id=UUIDFilter(eq=current_user_id))
```

**Modified** `get_dataset` — add visibility guard: if `PRIVATE` and requester ≠ owner → 404.

**Modified** `upload_dataset` — accept optional `visibility` form field (defaults to `PRIVATE`).

**New** `update_dataset` route — allows owner to toggle visibility (guarded by `can_edit_dataset`).

**`can_edit_dataset`** — no changes needed (already checks `owner_id`).

## Future Considerations

When teams/sharing are introduced:
- Add `TEAM` / `SHARED` values to the `DatasetVisibility` enum
- Create a separate `DatasetShare` join table `(dataset_id, grantee_type, grantee_id)` for granular access
- The listing query extends: `owner_id = me OR visibility = PUBLIC OR id IN (shared_with_me)`
- The `PUBLIC` visibility remains orthogonal to sharing — no refactoring needed
