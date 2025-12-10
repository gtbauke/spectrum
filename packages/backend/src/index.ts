import "dotenv/config";
import cors from "cors";
import express from "express";
import helmet from "helmet";
import { pinoHttp } from "pino-http";
import { logger } from "./logger.js";
import { ENV } from "./utils/env.util.js";

const app = express();

app.use(cors());
app.use(helmet());
app.use(
    pinoHttp({
        logger,
        autoLogging: true,
    }),
);

app.listen(ENV.PORT, () => {
    logger.info(`Server listening on port ${ENV.PORT}`);
});
