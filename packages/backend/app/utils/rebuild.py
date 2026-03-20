from __future__ import annotations

from core.models.users.user import User
from core.models.owners.owner import Owner
from core.models.auth.refresh_token import RefreshToken

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_version import DatasetVersion
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion

from core.models.profiles.profile import Profile
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation
from core.models.profiles.profile_block import ProfileBlock

from core.models.jobs.job import Job
from core.models.jobs.job_version import JobVersion

from core.models.job_runs.job_run import JobRun
from core.models.models.model import Model

namespace = {  # type: ignore
    "User": User,
    "Owner": Owner,
    "RefreshToken": RefreshToken,
    "Dataset": Dataset,
    "DatasetVersion": DatasetVersion,
    "DatasetArtifact": DatasetArtifact,
    "DatasetArtifactVersion": DatasetArtifactVersion,
    "Profile": Profile,
    "ProfileVersion": ProfileVersion,
    "ProfileDatasetAssociation": ProfileDatasetAssociation,
    "ProfileBlock": ProfileBlock,
    "Job": Job,
    "JobVersion": JobVersion,
    "JobRun": JobRun,
    "Model": Model,
}

for item in [
    User,
    Owner,
    RefreshToken,
    Dataset,
    DatasetVersion,
    DatasetArtifact,
    DatasetArtifactVersion,
    Profile,
    ProfileVersion,
    ProfileDatasetAssociation,
    ProfileBlock,
    Job,
    JobVersion,
    JobRun,
    Model,
]:
    item.model_rebuild(_types_namespace=namespace)
