from aws.ecs import ecs
from config import Config


def run_training_task(
    cluster_name: str,
    task_definition: str,
    container_name: str,
    env: dict[str, str],
):
    ecs.run_task(
        cluster=cluster_name,
        launchType="FARGATE",
        taskDefinition=task_definition,
        overrides={
            "containerOverrides": [
                {
                    "name": container_name,
                    "environment": [{"name": k, "value": v} for k, v in env.items()],
                }
            ]
        },
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": [Config.SUBNET_ID],
                "assignPublicIp": "ENABLED",
            }
        }
    )
