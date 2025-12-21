import { PublishCommand, SNSClient } from "@aws-sdk/client-sns";
import { ENV } from "./env.util.js";

const sns = new SNSClient({
    region: ENV.AWS_REGION,
});

export type DatasetUploadedEvent = {
    datasetId: string;
    bucket: string;
    key: string;
    uploadedAt: string;
};

export async function publishDatasetUploadedEvent(
    payload: DatasetUploadedEvent,
) {
    await sns.send(
        new PublishCommand({
            TopicArn: ENV.DATASET_UPLOADED_TOPIC_ARN,
            Message: JSON.stringify(payload),
            MessageAttributes: {
                eventType: {
                    DataType: "String",
                    StringValue: "dataset.uploaded",
                },
                version: {
                    DataType: "String",
                    StringValue: "1",
                },
            },
        }),
    );
}
