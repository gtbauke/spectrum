from models import Model, ModelStatus


def can_start_model_training(model: Model) -> bool:
    return model.status in [ModelStatus.PENDING, ModelStatus.FAILED]
