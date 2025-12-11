import "dotenv/config.js";
import { z } from "zod";

export type Simplify<
    T extends Record<string, unknown> = Record<string, unknown>,
> = {
    [K in keyof T]: T[K];
} & {};

export class EnvironmentValidationError extends Error {
    public constructor(errors: string[]) {
        super(`Invalid environment variables:\n${errors.join("\n")}`);
    }
}

export function getEnvironment<TSchema extends Record<string, z.ZodType>>(
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

export const ROOT_ENV = getEnvironment({
    DATABASE_URL: z.url(),
});
