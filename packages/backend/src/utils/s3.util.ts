import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { type BodyDataTypes, Upload } from "@aws-sdk/lib-storage";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { logger } from "~/logger.js";
import { ENV } from "./env.util.js";

const EXPIRES_IN_ONE_HOUR = 3600;

export const s3 = new S3Client({
    region: ENV.AWS_REGION,
    credentials: {
        accessKeyId: ENV.AWS_ACCESS_KEY_ID,
        secretAccessKey: ENV.AWS_SECRET_ACCESS_KEY,
    },
});

export type StreamUploadInput = {
    bucket: string;
    key: string;
    body: BodyDataTypes;
    contentType?: string;
    expiresInSeconds?: number;
};

export type StreamUploadResult = {
    key: string;
    url: string;
};

export async function streamToS3({
    body,
    bucket,
    key,
    contentType,
    expiresInSeconds = EXPIRES_IN_ONE_HOUR,
}: StreamUploadInput): Promise<StreamUploadResult> {
    logger.info(`Starting upload to S3 bucket: ${bucket}, key: ${key}`);
    logger.info(`Body: ${body}`);

    if (body === null || body === undefined) {
        throw new Error("Body cannot be null or undefined");
    }

    const upload = new Upload({
        client: s3,
        params: {
            Bucket: bucket,
            Key: key,
            Body: body,
            ContentType: contentType,
        },
    });

    await upload.done();

    const command = new GetObjectCommand({
        Bucket: bucket,
        Key: key,
    });

    const url = await getSignedUrl(s3, command, {
        expiresIn: expiresInSeconds,
    });

    return { key, url };
}
