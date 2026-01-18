import amqp from "amqplib";
import { logger } from "~b/logger.js";

export const TASK_QUEUE = "dataset_training_tasks";

// TODO: Load RabbitMQ connection URL from environment variables
const connection = await amqp.connect("amqp://localhost");
const channel = await connection.createChannel();

await channel.assertQueue(TASK_QUEUE, { durable: true });

export async function publishDatasetUploadedEvent(datasetId: string) {
    channel.sendToQueue(TASK_QUEUE, Buffer.from(datasetId), {
        persistent: true,
    });

    logger.info({ message: "Published dataset uploaded event", datasetId });
}
