from __future__ import annotations

from core.features.users.user import User
from core.features.auth.refresh_token import RefreshToken
from core.features.datasets.dataset import Dataset
from core.features.datasets.artifact import Artifact
from core.features.profiles.profile import Profile
from core.features.profiles.blocks.block import Block
from core.features.profiles.models.model import Model
from core.features.profiles.jobs.job import Job
from core.features.profiles.jobs.runs.run import Run
from core.features.profiles.blocks.inference.inference_result import InferenceResult
from core.features.profiles.blocks.inference.inference_run import InferenceRun
from core.features.profiles.where import ProfileFilter
from core.features.profiles.jobs.where import JobFilter
from core.features.profiles.jobs.runs.where import RunFilter

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

for item in [
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
]:
    item.model_rebuild(_types_namespace=namespace)
