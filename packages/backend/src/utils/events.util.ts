import amqp from "amqplib";
import { logger } from "~/logger.js";
import { ENV } from "./env.util.js";

const connection = await amqp.connect({
    hostname: ENV.RABBITMQ_HOST,
    port: ENV.RABBITMQ_PORT,
    username: ENV.RABBITMQ_USERNAME,
    password: ENV.RABBITMQ_PASSWORD,
});

// TODO: assert exchanges and queues on startup (need to declare everything the same way in all services)
const channel = await connection.createChannel();

export async function publishDatasetUploadedEvent(datasetId: string) {
    channel.sendToQueue(ENV.TASKS_QUEUE, Buffer.from(datasetId), {
        persistent: true,
    });

    logger.info({ message: "Published dataset uploaded event", datasetId });
}
