import type { Request, Response } from "express";

export type MiddlewareMutationMap<
    Body extends Record<string, unknown> = Record<string, unknown>,
    Context extends Record<string, unknown> = Record<string, unknown>,
> = {
    body?: Body;
    context?: Context;
};

export type Middleware<
    CIn extends MiddlewareMutationMap,
    COut extends MiddlewareMutationMap,
> = (input: CIn, req: Request, res: Response) => Promise<COut> | COut;

export function compose<
    C0 extends MiddlewareMutationMap,
    C1 extends MiddlewareMutationMap,
    C2 extends MiddlewareMutationMap,
>(m1: Middleware<C0, C1>, m2: Middleware<C1, C2>) {
    return [m1, m2];
}

export function ensure<
    C0 extends MiddlewareMutationMap,
    C1 extends MiddlewareMutationMap,
>(middleware: Middleware<C0, C1>) {
    return [middleware];
}
