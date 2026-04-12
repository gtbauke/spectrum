# Design Spec: S3 File Storage Integration

**Status**: Draft
**Author**: Antigravity
**Date**: 2026-04-12

## 1. Goal
The objective is to implement an S3-based storage adapter for the Spectrum platform, enabling production-ready file management (uploads/downloads) while maintaining a compatible local storage implementation for development. The system must support pre-signed URLs for direct client-to-storage interactions.

## 2. Architecture

### 2.1 Layer Isolation (DDD)
Following the project's Domain-Driven Design constraints:
- **Domain Layer (`packages/core`)**: Defines the updated `FileStorage` protocol and data models (`UploadResult`). No external dependencies (like `boto3`) will be added here.
- **Adapter Layer (`packages/backend`, `packages/workers`)**: Contains the concrete implementations (`S3FileStorage`, `LocalStorage`) and their respective dependencies.

### 2.2 Components

#### A. FileStorage Protocol (`core.ports.storage`)
Extended with async methods:
- `generate_upload_url(path: str, expiration: int) -> str`
- `generate_download_url(path: str, expiration: int) -> str`

#### B. S3FileStorage Implementation
- Uses `aioboto3` for non-blocking AWS S3 interactions.
- Handles pre-signed URL generation for both `PUT` (uploads) and `GET` (downloads).
- Implemented separately in `backend` and `workers` to allow package-level dependency management.

#### C. LocalFileStorage Implementation
- Updated to return URLs that point to a local static route during development.
- Uses `STORAGE_BASE_URL` from configuration to build these URLs.
- For `generate_upload_url`, it returns a backend endpoint that mimics S3's PUT behavior.

#### D. Static File Serving (Backend)
- A FastAPI `StaticFiles` route will be mounted at `/storage` (or similar) when `STORAGE_TYPE=local` is active.

## 3. Configuration

New settings in `packages/core/core/common/config.py`:
| Setting | Type | Description |
| :--- | :--- | :--- |
| `STORAGE_TYPE` | `Literal["local", "s3"]` | Determines which adapter to instantiate. |
| `STORAGE_BASE_URL` | `str` | Base URL for local storage links. |
| `S3_BUCKET` | `str` | AWS S3 Bucket name. |
| `S3_REGION` | `str` | AWS Region. |
| `S3_ACCESS_KEY` | `SecretStr` | AWS Credentials. |
| `S3_SECRET_KEY` | `SecretStr` | AWS Credentials. |
| `S3_ENDPOINT_URL`| `str` (Optional) | For MinIO or S3-compatible services in dev. |

## 4. Implementation Details

### 4.1 Dependency Updates
- **backend**: Add `aioboto3`.
- **workers**: Add `aioboto3`.

### 4.2 Security
- S3 URLs will use appropriate expiration times (default 3600s).
- AWS Credentials will be managed via Pydantic `SecretStr`.

## 5. Testing & Verification
- Unit tests for both storage implementations.
- Integration tests in development using local storage and static routing.
- (Optional) Verification against a MinIO container to simulate S3 behavior.
