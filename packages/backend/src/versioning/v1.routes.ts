import { Router } from "express";
import { datasetsRouter } from "~/datasets/datasets.routes.js";

export const v1Router = Router();

v1Router.use("/datasets", datasetsRouter);
