import { z } from "zod";
import type { Simplify } from "~b/types/simplify.type.js";

const LOG_LEVELS = ["trace", "debug", "info", "warn", "error", "fatal"];
const LOG_LEVEL_NUMBERS = [10, 20, 30, 40, 50, 60];

const DEV_ENVS = ["dev", "development"];
const PROD_ENVS = ["prod", "production"];
const TEST_ENVS = ["test", "homolog"];

const ALL_ENVS = [...DEV_ENVS, ...PROD_ENVS, ...TEST_ENVS];

class EnvironmentValidationError extends Error {
    public constructor(errors: string[]) {
        super(`Invalid environment variables:\n${errors.join("\n")}`);
    }
}

function getEnvironment<TSchema extends Record<string, z.ZodType>>(
    schema: TSchema,
): Simplify<z.infer<z.ZodObject<TSchema>>> {
    const validatedEnv = z.object(schema).safeParse(process.env);
    if (!validatedEnv.success) {
        const finalErrors = validatedEnv.error.issues.map((issue) => {
            const path = issue.path.join(".");
            return `${path}: ${issue.message}`;
        });

        throw new EnvironmentValidationError(finalErrors);
    }

    return validatedEnv.data;
}

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
});

export function isDev() {
    return DEV_ENVS.includes(ENV.NODE_ENV);
}
