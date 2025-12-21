import { Router } from "express";
import z from "zod";
import { logger } from "~b/logger.js";
import { prisma } from "~b/prisma.service.js";
import { ENV } from "~b/utils/env.util.js";
import {
    compose,
    parseJsonFields,
    type StreamedFile,
    streamFiles,
    typedRoute,
} from "~b/utils/request.util.js";
import { streamToS3 } from "~b/utils/s3.util.js";
import { upload } from "~b/utils/upload.util.js";
import { createDatasetValidator } from "~shared/datasets.validator.js";
import { DatasetsService } from "./datasets.service.js";

export const datasetsRouter = Router();

const datasetsService = new DatasetsService({ prisma });

datasetsRouter.get("/", async (_, res) => {
    const data = await datasetsService.getAll({});
    return res.status(200).json({ data });
});

const validator = {
    body: createDatasetValidator,
};

// TODO: fix title field parsing
datasetsRouter.post(
    "/",
    upload.fields([
        { name: "dataset", maxCount: 1 },
        { name: "title", maxCount: 1 },
    ]),
    typedRoute<
        {
            files: {
                dataset: StreamedFile;
            };
        },
        typeof validator
    >(
        validator,
        compose(
            parseJsonFields({
                title: z.string(),
            }),
            streamFiles<{
                dataset: StreamedFile;
            }>({
                dataset: {
                    mimeTypes: ["text/csv"],
                    required: true,
                },
            }),
        ),
        async ({ body }, context, res) => {
            const { dataset: datasetFile } = context.files;
            logger.info(
                `Uploading dataset file: ${datasetFile.originalName}, size: ${datasetFile.size} bytes`,
            );

            const key = `datasets/${Date.now()}_${datasetFile.originalName}`;

            const { url } = await streamToS3({
                bucket: ENV.S3_BUCKET_NAME,
                key,
                body: datasetFile.stream as any,
                contentType: datasetFile.mimeType,
            });

            const dataset = await datasetsService.create({
                title: body.title,
                fileUrl: url,
            });

            return res.status(201).json({ data: dataset });
        },
    ),
);
