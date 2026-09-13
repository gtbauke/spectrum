from __future__ import annotations

from pydantic import BaseModel

from app.features.users.domain.user import User
from app.features.auth.domain.refresh_token import RefreshToken
from app.features.datasets.domain.dataset import Dataset
from app.features.datasets.domain.artifact import Artifact
from app.features.profiles.domain.profile import Profile
from app.features.profiles.blocks.domain.block import Block
from app.features.profiles.models.domain.model import Model
from app.features.profiles.jobs.domain.job import Job
from app.features.profiles.jobs.runs.domain.run import Run
from app.features.profiles.blocks.inference.domain.inference_result import InferenceResult
from app.features.profiles.blocks.inference.domain.inference_run import InferenceRun
from app.features.profiles.domain.where import ProfileFilter
from app.features.profiles.jobs.domain.where import JobFilter
from app.features.profiles.jobs.runs.domain.where import RunFilter

namespace = {  # type: ignore
    "User": User,
    "RefreshToken": RefreshToken,
    "Dataset": Dataset,
    "Artifact": Artifact,
    "Profile": Profile,
    "Block": Block,
    "Model": Model,
    "Job": Job,
    "Run": Run,
    "InferenceResult": InferenceResult,
    "InferenceRun": InferenceRun,
    "ProfileFilter": ProfileFilter,
    "JobFilter": JobFilter,
    "RunFilter": RunFilter,
}

models_to_rebuild: list[type[BaseModel]] = [
    User,
    RefreshToken,
    Dataset,
    Artifact,
    Profile,
    Block,
    Model,
    Job,
    Run,
    InferenceResult,
    InferenceRun,
    ProfileFilter,
    JobFilter,
    RunFilter,
]

for item in models_to_rebuild:
    item.model_rebuild(_types_namespace=namespace)
