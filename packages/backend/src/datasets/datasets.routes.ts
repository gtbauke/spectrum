import { Router } from "express";
import { prisma } from "~b/prisma.service.js";
import { ENV } from "~b/utils/env.util.js";
import { HTTP_CODES } from "~b/utils/http.util.js";
import { ensure } from "~b/utils/middleware.util.js";
import { typedPipeline } from "~b/utils/request.util.js";
import { streamToS3 } from "~b/utils/s3.util.js";
import { streamFiles } from "~b/utils/stream.util.js";
import { upload } from "~b/utils/upload.util.js";
import { DatasetsService } from "./datasets.service.js";
import {
    type CreateDatasetContext,
    type CreateDatasetRequestValidator,
    createDatasetRequestValidator,
} from "./datasets.validator.js";

export const datasetsRouter = Router();

const datasetsService = new DatasetsService({ prisma });

datasetsRouter.get("/", async (_, res) => {
    const data = await datasetsService.getAll({});
    return res.status(HTTP_CODES.OK).json({ data });
});

datasetsRouter.post(
    "/",
    upload.fields([
        { name: "dataset", maxCount: 1 },
        { name: "title", maxCount: 1 },
    ]),
    typedPipeline<CreateDatasetContext, CreateDatasetRequestValidator>(
        createDatasetRequestValidator,
        ensure(
            streamFiles<CreateDatasetContext["files"]>({
                dataset: {
                    mimeTypes: ["text/csv"],
                    required: true,
                },
            }),
        ),
        async ({ body }, context, res) => {
            const { dataset: datasetFile } = context.files;
            const key = `datasets/${Date.now()}_${datasetFile.originalName}`;

            const { url } = await streamToS3({
                bucket: ENV.S3_BUCKET_NAME,
                key,
                body: datasetFile.stream,
                contentType: datasetFile.mimeType,
            });

            const dataset = await datasetsService.create({
                title: body.title,
                fileUrl: url,
            });

            return res.status(HTTP_CODES.CREATED).json({ data: dataset });
        },
    ),
);
