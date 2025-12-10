export type Simplify<
    T extends Record<string, unknown> = Record<string, unknown>,
> = {
    [K in keyof T]: T[K];
} & {};
