/** biome-ignore-all lint/suspicious/noExplicitAny: This file uses `any` in order to handle unknown shapes of requests */
import type { NextFunction, Request, RequestHandler, Response } from "express";
import { z } from "zod";
import type { SafeOmit } from "~/types/safe-omit.type.js";
import { HTTP_CODES } from "./http.util.js";
import type { Middleware, MiddlewareMutationMap } from "./middleware.util.js";

export const MULTIPART_FORM_DATA = "multipart/form-data";

type PartialSchema = {
    body?: z.ZodType;
    query?: z.ZodType;
    params?: z.ZodType;
};

type RequestHandlerData<T extends PartialSchema> = {
    partialSchema: T;
    middlewares: Middleware<MiddlewareMutationMap, MiddlewareMutationMap>[];
    handler: (
        data: z.infer<z.ZodObject<T>>,
        context: any,
        res: Response,
    ) => any;
    request: Request;
    response: Response;
    next: NextFunction;
};

function parseRequestBody<T extends Record<string, unknown>>(body: T) {
    const parsedBody: Partial<Record<keyof T, unknown>> = {};

    for (const key in body) {
        if (typeof body[key] !== "string") {
            continue;
        }

        const value = JSON.parse(body[key]);
        parsedBody[key] = value;
    }

    return parsedBody;
}

async function handleMiddlewaresAndRequest<T extends PartialSchema>({
    handler,
    middlewares,
    request,
    response,
    result,
}: SafeOmit<RequestHandlerData<T>, "partialSchema" | "next"> & {
    result: z.infer<z.ZodObject<T>>;
}) {
    let context = {};
    let body = result || {};

    for (const mw of middlewares) {
        const result = await mw(context, request, response);

        context = { ...result.context, ...context };
        body = { ...body, ...result.body };
    }

    return handler(result, context, response);
}

async function handleMultipartRequest<T extends PartialSchema>({
    handler,
    middlewares,
    next,
    partialSchema,
    request,
    response,
}: RequestHandlerData<T>) {
    try {
        const schema = z.object(partialSchema);
        const result = schema.safeParse({
            body: parseRequestBody(request.body),
            query: request.query,
            params: request.params,
        });

        if (!result.success) {
            return response.status(HTTP_CODES.BAD_REQUEST).json({
                error: "Validation Error",
                details: z.treeifyError(result.error),
            });
        }

        handleMiddlewaresAndRequest({
            handler,
            middlewares,
            request,
            response,
            result: result.data,
        });
    } catch (error) {
        next(error);
    }
}

async function handleNonMultipartRequest<T extends PartialSchema>({
    handler,
    middlewares,
    next,
    partialSchema,
    request,
    response,
}: RequestHandlerData<T>) {
    try {
        const schema = z.object(partialSchema);
        const result = schema.safeParse({
            body: request.body,
            query: request.query,
            params: request.params,
        });

        if (!result.success) {
            return response.status(HTTP_CODES.BAD_REQUEST).json({
                error: "Validation Error",
                details: z.treeifyError(result.error),
            });
        }

        handleMiddlewaresAndRequest({
            handler,
            middlewares,
            request,
            response,
            result: result.data,
        });
    } catch (error) {
        next(error);
    }
}

export function typedPipeline<Context, T extends PartialSchema>(
    partialSchema: T,
    middlewares: Middleware<any, any>[],
    handler: (
        data: z.infer<z.ZodObject<T>>,
        context: Context,
        res: Response,
    ) => any,
): RequestHandler {
    return async (req: Request, res: Response, next: NextFunction) => {
        const contentType = req.headers["content-type"] || "";

        if (contentType.includes(MULTIPART_FORM_DATA)) {
            handleMultipartRequest({
                handler,
                middlewares,
                next,
                partialSchema,
                request: req,
                response: res,
            });

            return;
        }

        handleNonMultipartRequest({
            handler,
            middlewares,
            next,
            partialSchema,
            request: req,
            response: res,
        });
    };
}
