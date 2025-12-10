import { pino } from "pino";
import { ENV, isDev } from "./utils/env.util.js";

export const logger = pino({
    level: ENV.LOG_LEVEL,
    ...(isDev() && {
        transport: {
            target: "pino-pretty",
            options: {
                colorize: true,
                translateTime: "SYS:standard",
                ignore: "pid,hostname",
            },
        },
    }),
});
