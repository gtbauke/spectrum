import { Router } from "express";
import { datasetsRouter } from "~b/datasets/datasets.routes.js";

export const v1Router = Router();

v1Router.use("/datasets", datasetsRouter);
