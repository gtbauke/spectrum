import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from core.features.profiles.blocks.inference.events import InferenceRunRequestedEvent
from handlers.inference_run_requested import InferenceRunRequestedHandler
from core.features.profiles.blocks.block_kind import BlockKind
from core.features.profiles.models.model import Model
from core.features.profiles.jobs.job import Job
from core.features.datasets.dataset import Dataset
from core.features.datasets.artifact import Artifact
from core.features.datasets.artifact_role import ArtifactRole

class TestInferencePipeline(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.broker = MagicMock()
        self.handler = InferenceRunRequestedHandler(broker=self.broker)

    @patch("handlers.inference_run_requested.WorkerUnitOfWork")
    @patch("handlers.inference_run_requested.Reggression")
    @patch("handlers.inference_run_requested.QueryExecutor")
    @patch("handlers.inference_run_requested.os.path.join")
    @patch("handlers.inference_run_requested.tempfile.TemporaryDirectory")
    async def test_handle_success(self, mock_tmp_dir, mock_path_join, mock_executor_cls, mock_reggression_cls, mock_uow_cls):
        # Setup Event
        run_id = uuid4()
        block_id = uuid4()
        profile_id = uuid4()
        event = InferenceRunRequestedEvent(
            run_id=run_id,
            block_id=block_id,
            profile_id=profile_id,
            query="SELECT id, fitness FROM my_model"
        )

        # Setup Mocks
        mock_uow = AsyncMock()
        mock_uow_cls.return_value.__aenter__.return_value = mock_uow
        
        # Mock Model resolution
        model_id = uuid4()
        mock_model = MagicMock(spec=Model)
        mock_model.id = model_id
        mock_model.name = "my_model"
        mock_model.generated_by = uuid4()
        mock_model.path = "models/model.egraph"
        
        mock_uow.models.list_all.return_value = [mock_model]
        
        # Mock Job resolution
        mock_job = MagicMock(spec=Job)
        mock_job.runs_against = uuid4()
        mock_uow.jobs.get_unique.return_value = mock_job
        
        # Mock Dataset resolution
        mock_dataset = MagicMock(spec=Dataset)
        mock_artifact = MagicMock(spec=Artifact)
        mock_artifact.role = ArtifactRole.DATA
        mock_artifact.path = "datasets/data.csv"
        mock_dataset.artifacts = [mock_artifact]
        mock_uow.datasets.get_unique.return_value = mock_dataset
        
        # Mock temp dir
        mock_tmp_dir.return_value.__enter__.return_value = "/tmp/fake"
        mock_path_join.side_effect = lambda a, b: f"{a}/{b}"
        
        # Mock Executor
        mock_executor = MagicMock()
        mock_executor_cls.return_value = mock_executor
        mock_result = MagicMock()
        mock_result.results = [
            MagicMock(expression="x + 1", fitness=0.9, latex="x+1", numpy="x+1", parameters={})
        ]
        mock_executor.execute.return_value = mock_result

        # Run Handler
        await self.handler.handle(event)

        # Verifications
        mock_uow.models.list_all.assert_called()
        mock_uow.file_storage.download.assert_any_call(path="datasets/data.csv", destination="/tmp/fake/dataset.csv")
        mock_uow.file_storage.download.assert_any_call(path="models/model.egraph", destination="/tmp/fake/model.egraph")
        mock_reggression_cls.assert_called_with(dataset="/tmp/fake/dataset.csv", loadFrom="/tmp/fake/model.egraph")
        mock_uow.inference_results.add_many.assert_called_once()
        print("\nVerification successful: Handler correctly orchestrated the execution pipeline.")

if __name__ == "__main__":
    unittest.main()
