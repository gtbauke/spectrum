import { Router } from "express";
import { prisma } from "~b/prisma.service.js";
import { DatasetsService } from "./datasets.service.js";

export const datasetsRouter = Router();

const datasetsService = new DatasetsService({ prisma });

datasetsRouter.get("/", async (_, res) => {
    const data = await datasetsService.getAll({});
    return res.status(200).json({ data });
});
