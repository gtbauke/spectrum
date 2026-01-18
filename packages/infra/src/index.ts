import "dotenv/config";
import path from "node:path";
import { ENV } from "./utils/env.util.js";
import { EnvironmentBuilder } from "./utils/environment-builder.util.js";

const BACKEND_PACKAGE_PATH = path.resolve(
    import.meta.dirname,
    "..",
    "..",
    "backend",
);

const MODEL_RUNNER_PACKAGE_PATH = path.resolve(
    import.meta.dirname,
    "..",
    "..",
    "model-runner",
);

async function buildSharedEnvironment() {
    const sharedBuilder = new EnvironmentBuilder();

    sharedBuilder.set("RABBITMQ_HOST", "localhost");
    sharedBuilder.set("RABBITMQ_PORT", "5672");
    sharedBuilder.set("RABBITMQ_USERNAME", "guest");
    sharedBuilder.set("RABBITMQ_PASSWORD", "guest");

    sharedBuilder.set("TASKS_EXCHANGE", "tasks_exchange");
    sharedBuilder.set("TASKS_RETRY_EXCHANGE", "tasks_retry_exchange");
    sharedBuilder.set(
        "TASKS_DEAD_LETTER_EXCHANGE",
        "tasks_dead_letter_exchange",
    );
    sharedBuilder.set("TASKS_STATUS_EXCHANGE", "tasks_status_exchange");

    sharedBuilder.set("TASKS_QUEUE", "tasks_queue");
    sharedBuilder.set("TASKS_RETRY_QUEUE", "tasks_retry_queue");
    sharedBuilder.set("TASKS_DEAD_LETTER_QUEUE", "tasks_dead_letter_queue");
    sharedBuilder.set("TASKS_STATUS_QUEUE", "tasks_status_queue");

    sharedBuilder.set("AWS_REGION", ENV.AWS_REGION);
    sharedBuilder.set("AWS_ACCESS_KEY_ID", ENV.AWS_ACCESS_KEY_ID);
    sharedBuilder.set("AWS_SECRET_ACCESS_KEY", ENV.AWS_SECRET_ACCESS_KEY);
    sharedBuilder.set("S3_BUCKET_NAME", ENV.S3_BUCKET_NAME);

    sharedBuilder.set("DATABASE_URL", ENV.DATABASE_URL);

    await sharedBuilder.build(path.join(BACKEND_PACKAGE_PATH, ".env"));
    await sharedBuilder.build(path.join(MODEL_RUNNER_PACKAGE_PATH, ".env"));
}

async function main() {
    await buildSharedEnvironment();
}

main()
    .then(() => {})
    .catch((err) => {
        console.error(err);
        process.exit(1);
    });
