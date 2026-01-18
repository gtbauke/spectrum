import { z } from "zod";
import { getEnvironment, ROOT_ENV } from "~utils/root-env.util.js";

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
});

export function isDev() {
    return DEV_ENVS.includes(ENV.NODE_ENV);
}
