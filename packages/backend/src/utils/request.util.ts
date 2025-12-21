/** biome-ignore-all lint/suspicious/noExplicitAny: This file uses `any` in order to handle unknown shapes of requests */
import type { NextFunction, Request, RequestHandler, Response } from "express";
import { z } from "zod";
import { logger } from "~b/logger.js";

export type Middleware<CIn, COut> = (
    ctx: CIn,
    req: Request,
    res: Response,
) => Promise<COut> | COut;

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
