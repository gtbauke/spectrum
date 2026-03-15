import { z } from "zod";

export const lossFunctionValues = [
	"MSE",
	"Gaussian",
	"Bernoulli",
	"Poisson",
] as const;
export const lossFunctionSchema = z.enum(lossFunctionValues);

export type LossFunction = z.infer<typeof lossFunctionSchema>;
