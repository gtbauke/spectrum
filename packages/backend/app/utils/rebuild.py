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
    "ProfileDatasetAssociation": ProfileDatasetAssociation
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
    ProfileDatasetAssociation
]:
    item.model_rebuild(_types_namespace=namespace)
