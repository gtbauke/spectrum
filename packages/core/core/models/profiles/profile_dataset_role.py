from enum import StrEnum


class ProfileDatasetRole(StrEnum):
    TRAINING = "training"
    TESTING = "testing"
    VALIDATING = "validating"
