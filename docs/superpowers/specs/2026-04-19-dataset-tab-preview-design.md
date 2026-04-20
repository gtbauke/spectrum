# Dataset Tab Metadata & Data Preview Design

## 1. UI Architecture
We will update `DatasetTabContainer` to support inline editing for the dataset's metadata (Name and Description) and to display a paginated preview of its associated artifacts. 

- **Layout Structure:** We will maintain the existing full-width header. Underneath, we'll split the main content area into a two-pane layout: a main visualizer taking up approx 75% of the width, and a sidebar list taking up the remaining 25%.
- **Right Sidebar:** A scrollable list showing the `Artifact` entries associated with this dataset. It will mimic the look-and-feel of the list in the Model Insights section. Clicking an artifact will set it as the "active" data preview in the left pane.
- **Left Main Area:** 
  - **Data Preview:** Employs the existing `DatasetPreviewTable` to present the CSV content of the selected artifact.
  - **Pagination Controls:** Next/Previous buttons and a "Rows per page" limiter will be anchored below the table to handle large datasets.
- **Metadata Inline Editing:** In the top header, the dataset Name and Description will support inline editing. Clicking the text will transform it into an input/textarea. Changes will be saved via the new `PUT` backend endpoint when the user hits Enter or clicks away.

## 2. Backend Architecture
To support the UI needs, two new routes will be introduced:

- **Update Dataset Route:**
  - **Route:** `PUT /datasets/{dataset_id}`
  - **Purpose:** Updates the `name` and `description` fields on the `Dataset` domain model.
  - **Consistency:** By using `PUT`, this endpoint matches the established DDD update pattern utilized by other resource routers (e.g., profiles, jobs).

- **Data Preview Route:**
  - **Route:** `GET /datasets/{dataset_id}/artifacts/{artifact_id}/preview`
  - **Purpose:** Supplies the paginated CSV data for the frontend preview table.
  - **Parameters:** `limit` (integer, default=50) and `offset` (integer, default=0).
  - **Implementation Strategy:** Validates permissions with `can_edit_dataset` / `get_current_user`, seamlessly downloads the requested artifact to a temporary path via `uow.file_storage.download()`, parses and slices the CSV data utilizing a high-performance dataframe library (`polars`), outputs the expected `DatasetPreviewTable` format `{"columns": [...], "data": [...], "total": int}`, and handles cleanup.

## 3. Trade-offs & Considerations
- **On-the-fly Download vs. Sample Caching:** We are opting to pull and parse the CSV on the fly via `FileStorage.download`. This trades absolute latency for architectural simplicity. Given that current target environments (like fast S3/local connections) handle moderate-sized datasets efficiently and symbolic regression primarily trains on relatively compact numeric inputs, dynamic slicing is a highly robust solution. If datasets significantly grow in size, predicting long latency for full-file downloads, caching an explicit "head snippet" at initial upload would be the optimization path forward.
