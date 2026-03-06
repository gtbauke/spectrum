from enum import StrEnum


class ArtifactType(StrEnum):
    DATA = "data"
    SCHEMA = "schema"
    STATS = "stats"
    PREVIEW = "preview"
    FEATURES = "features"
