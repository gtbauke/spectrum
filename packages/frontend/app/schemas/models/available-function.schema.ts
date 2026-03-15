import { z } from "zod";

export const availableFunctionValues = [
	"add",
	"sub",
	"mul",
	"div",
	"power",
	"powerabs",
	"square",
	"cube",
	"sqrt",
	"sqrtabs",
	"cbrt",
	"sin",
	"cos",
	"tan",
	"asin",
	"acos",
	"atan",
	"sinh",
	"cosh",
	"tanh",
	"asinh",
	"acosh",
	"atanh",
	"abs",
	"log",
	"logabs",
	"exp",
	"recip",
	"aq",
] as const;
export const availableFunctionSchema = z.enum(availableFunctionValues);

export type AvailableFunction = z.infer<typeof availableFunctionSchema>;
