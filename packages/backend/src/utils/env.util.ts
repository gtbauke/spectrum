import { z } from "zod";
import { getEnvironment, ROOT_ENV } from "~utils/root-env.util.js";

const LOG_LEVELS = ["trace", "debug", "info", "warn", "error", "fatal"];
const LOG_LEVEL_NUMBERS = [10, 20, 30, 40, 50, 60];

const DEV_ENVS = ["dev", "development"];
const PROD_ENVS = ["prod", "production"];
const TEST_ENVS = ["test", "homolog"];

const ALL_ENVS = [...DEV_ENVS, ...PROD_ENVS, ...TEST_ENVS];

export const ENV = getEnvironment({
    PORT: z
        .string()
        .default("3000")
        .transform((v) => Number.parseInt(v, 10))
        .pipe(z.number()),

    LOG_LEVEL: z
        .union([
            z.enum(LOG_LEVELS),
            z
                .number()
                .int()
                .refine((v) => LOG_LEVEL_NUMBERS.includes(v)),
        ])
        .transform((v) => {
            if (typeof v === "number") {
                const index = LOG_LEVEL_NUMBERS.indexOf(v);
                return LOG_LEVELS[index];
            }

            return v;
        })
        .default("info"),

    NODE_ENV: z
        .enum(ALL_ENVS)
        .default("dev")
        .transform((v) => {
            if (DEV_ENVS.includes(v)) return "dev";
            if (PROD_ENVS.includes(v)) return "prod";
            if (TEST_ENVS.includes(v)) return "test";

            return v;
        })
        .default("dev"),

    DATABASE_URL: z.string().default(ROOT_ENV.DATABASE_URL),
    AWS_REGION: z.string(),
    AWS_ACCESS_KEY_ID: z.string(),
    AWS_SECRET_ACCESS_KEY: z.string(),
    S3_BUCKET_NAME: z.string(),

    RABBITMQ_HOST: z.string().default("localhost"),
    RABBITMQ_PORT: z
        .string()
        .default("5672")
        .transform((v) => Number.parseInt(v, 10))
        .pipe(z.number()),
    RABBITMQ_USERNAME: z.string().default("guest"),
    RABBITMQ_PASSWORD: z.string().default("guest"),

    TASKS_EXCHANGE: z.string(),
    TASKS_RETRY_EXCHANGE: z.string(),
    TASKS_DEAD_LETTER_EXCHANGE: z.string(),
    TASKS_STATUS_EXCHANGE: z.string(),

    TASKS_EXCHANGE_ROUTING_KEY: z.string(),
    TASKS_RETRY_ROUTING_KEY: z.string(),
    TASKS_DEAD_LETTER_ROUTING_KEY: z.string(),

    TASKS_QUEUE: z.string(),
    TASKS_RETRY_QUEUE: z.string(),
    TASKS_DEAD_LETTER_QUEUE: z.string(),
    TASKS_STATUS_QUEUE: z.string(),
});

export function isDev() {
    return DEV_ENVS.includes(ENV.NODE_ENV);
}
