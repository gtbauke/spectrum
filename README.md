# Spectrum

Spectrum is an web platform for managing Symbolic Regression models, enabling model inference in real-time via WebSockets. The tool is similar to HeuristicsLabs and TuringBot but is designed to be more user-friendly and accessible.

## How it is built?

Spectrum is built around an event-driven architecture with async workers for dataset pre-processing and model training. The backend is developed using FastAPI, while the frontend is created with ReactJS. Real-time communication is facilitated through WebSockets.

## Architecture Overview

The architecture consists of the following components:

- **Frontend**: A ReactJS application that provides a user interface for managing datasets, training models, and making predictions.
- **Backend**: A FastAPI server that handles API requests, manages WebSocket connections, and orchestrates the training and inference processes.
- **Async Workers**: Background workers that process datasets and train models asynchronously to ensure responsiveness.
- **Database**: A storage solution for persisting datasets, models, and user information.

## Pre-requisites

To run Spectrum locally, ensure you have the following installed:

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [Node.js](https://nodejs.org/) (for frontend development)
- [PostgreSQL](https://www.postgresql.org/)

### Installation

1. Install python
2. Install and run RabbitMQ server
3. Install and run PostgreSQL server
4. Install uv: `pip install uv`
5. Clone the repository: `git clone git@github.com:gtbauke/spectrum.git`
6. Navigate to the project directory: `cd spectrum`
7. Install backend dependencies: `uv sync --all-packages`
8. Install frontend dependencies: `cd packages/frontend && npm install`

### Running Spectrum

1. From the project root, start the backend server:

   ```bash
   uv run --package backend fastapi dev packages/backend/app/main.py
   ```

2. In a separate terminal, cd to `packages/backend`, start the dataset pre-processing worker:

   ```bash
   uv run python -m app.workers.orchestrators.datasets.dataset_processing_orchestrator
   ```

3. In another terminal, cd to `packages/backend`, start the model training worker:

   ```bash
   uv run python -m app.workers.orchestrators.models.model_processing_orchestrator
   ```

4. Finally, in another terminal, cd to `packages/frontend`, start the frontend development server:

   ```bash
   npm run dev
   ```

## Usage

Once all services are running, open your web browser and navigate to `http://localhost:5173/datasets/create` to access the Spectrum web interface. From here, you can create datasets, train Symbolic Regression models, and perform real-time inference using WebSockets.

## Project Structure

The project is organized into the following directories:

- `packages/backend`: Contains the FastAPI backend code, including API routes, WebSocket handlers, and async workers.
- `packages/frontend`: Contains the ReactJS frontend code, including components, pages, and styles
