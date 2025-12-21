import { Router } from "express";
import { prisma } from "~b/prisma.service.js";
import { typedRoute } from "~b/utils/request.util.js";
import { createDatasetValidator } from "~shared/datasets.validator.js";
import { DatasetsService } from "./datasets.service.js";

export const datasetsRouter = Router();

const datasetsService = new DatasetsService({ prisma });

datasetsRouter.get("/", async (_, res) => {
    const data = await datasetsService.getAll({});
    return res.status(200).json({ data });
});

datasetsRouter.post(
    "/",
    typedRoute(
        {
            body: createDatasetValidator,
        },
        [],
        async ({ body }, context, res) => {
            const dataset = await datasetsService.create(body);
            return res.status(201).json({ data: dataset });
        },
    ),
);
