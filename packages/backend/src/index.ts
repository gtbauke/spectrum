import "dotenv/config";

import cors from "cors";
import express from "express";
import helmet from "helmet";
import { pinoHttp } from "pino-http";
import { logger } from "./logger.js";
import { prisma } from "./prisma.service.js";
import { ENV } from "./utils/env.util.js";

async function main() {
    const app = express();

    app.use(cors());
    app.use(helmet());
    app.use(
        pinoHttp({
            logger,
            autoLogging: true,
        }),
    );

    app.get("/", async (_, res) => {
        const allDatasets = await prisma.dataset.findMany();
        logger.info(`All datasets: ${JSON.stringify(allDatasets, null, 4)}`);

        return res.status(200);
    });

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
