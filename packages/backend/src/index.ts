import "dotenv/config";

import cors from "cors";
import express from "express";
import helmet from "helmet";
import { pinoHttp } from "pino-http";
import { logger } from "./logger.js";
import { prisma } from "./prisma.service.js";
import { ENV } from "./utils/env.util.js";
import { v1Router } from "./versioning/v1.routes.js";

async function main() {
    const app = express();
    app.use(express.json());

    app.use(cors());
    app.use(helmet());
    app.use(
        pinoHttp({
            logger,
            autoLogging: true,
        }),
    );

    app.use("/api/v1", v1Router);

    app.listen(ENV.PORT, () => {
        logger.info(`Server listening on port ${ENV.PORT}`);
    });
}

main()
    .then(async () => {
        await prisma.$disconnect();
    })
    .catch(async (e) => {
        logger.error(e);
        await prisma.$disconnect();
        process.exit(1);
    });
