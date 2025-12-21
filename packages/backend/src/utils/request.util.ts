/** biome-ignore-all lint/suspicious/noExplicitAny: This file uses `any` in order to handle unknown shapes of requests */
import type { NextFunction, Request, RequestHandler, Response } from "express";
import { Readable } from "stream";
import { file, z } from "zod";
import { logger } from "~b/logger.js";

export type Middleware<CIn, COut> = (
    ctx: CIn,
    req: Request,
    res: Response,
) => Promise<COut> | COut;

export function compose<C0, C1, C2>(
    m1: Middleware<C0, C1>,
    m2: Middleware<C1, C2>,
) {
    return [m1, m2];
}

export function ensure<C0, C1>(middleware: Middleware<C0, C1>) {
    return [middleware];
}

export function typedRoute<
    Context,
    T extends {
        body?: z.ZodType;
        query?: z.ZodType;
        params?: z.ZodType;
    },
>(
    partialSchema: T,
    middlewares: Middleware<any, any>[],
    handler: (
        data: z.infer<z.ZodObject<T>>,
        context: Context,
        res: Response,
    ) => any,
): RequestHandler {
    return async (req: Request, res: Response, next: NextFunction) => {
        logger.info({
            message: "Received request for typed route",
            route: req.path,
            method: req.method,
            body: req.body,
            contentType: req.headers["content-type"],
        });

        try {
            logger.info({
                message: "Typed route pipeline started",
                route: req.path,
                method: req.method,
                body: req.body,
                query: req.query,
                params: req.params,
            });

            const schema = z.object(partialSchema);
            const result = schema.safeParse({
                body: req.body,
                query: req.query,
                params: req.params,
            });

            logger.info({
                message: "Validation result",
                success: result.success,
                errors: result.success ? null : result.error,
            });

            if (!result.success) {
                return res.status(400).json({
                    error: "Validation Error",
                    details: z.treeifyError(result.error),
                });
            }

            let context: any = {};
            for (const mw of middlewares) {
                context = await mw(context, req, res);
            }

            return handler(result.data, context, res);
        } catch (error) {
            next(error);
        }
    };
}

export type StreamedFile = {
    stream: NodeJS.ReadableStream;
    mimeType: string;
    originalName: string;
    size?: number;
};

type FileContext<T> = {
    files: T;
};

export class MissingRequiredFileError extends Error {
    public constructor(fileField: string) {
        super(`Missing required file: ${fileField}`);
        this.name = "MissingRequiredFileError";
    }
}

export class InvalidMimeTypeError extends Error {
    public constructor(
        fileField: string,
        expectedTypes: string[],
        actualType: string,
    ) {
        super(
            `Invalid MIME type for file ${fileField}: expected one of [${expectedTypes.join(
                ", ",
            )}], but got ${actualType}`,
        );
        this.name = "InvalidMimeTypeError";
    }
}

export function streamFiles<T extends Record<string, StreamedFile>>(
    rules: {
        [K in keyof T]: {
            required?: boolean;
            mimeTypes?: string[];
        };
    },
): Middleware<{}, FileContext<T>> {
    return async (_, req) => {
        const multerFiles = req.files as
            | Record<string, Express.Multer.File[]>
            | undefined;

        const files: Partial<Record<keyof T, StreamedFile>> = {};

        for (const field in rules) {
            const rule = rules[field];
            const fileArray = multerFiles?.[field];

            const file = fileArray?.[0];

            if (rule.required && !file) {
                throw new MissingRequiredFileError(field);
            }

            if (!file) {
                continue;
            }

            if (rule.mimeTypes && !rule.mimeTypes.includes(file.mimetype)) {
                throw new InvalidMimeTypeError(
                    field,
                    rule.mimeTypes,
                    file.mimetype,
                );
            }

            files[field] = {
                stream: Readable.from(file.buffer),
                mimeType: file.mimetype,
                originalName: file.originalname,
                size: file.size,
            };
        }

        return { files: files as T };
    };
}

export function parseJsonFields<T extends Record<string, z.ZodType>>(
    schemas: T,
): Middleware<{}, any> {
    return async (_, req) => {
        const parsedData: Partial<Record<keyof T, any>> = {};

        for (const field in schemas) {
            const rawValue = req.body[field];

            if (typeof rawValue !== "string") {
                throw new Error(
                    `Field ${field} is not a string and cannot be parsed as JSON`,
                );
            }

            try {
                parsedData[field] = JSON.parse(rawValue);
            } catch (error) {
                throw new Error(
                    `Failed to parse field ${field} as JSON: ${(error as Error).message}`,
                );
            }
        }

        return parsedData;
    };
}
