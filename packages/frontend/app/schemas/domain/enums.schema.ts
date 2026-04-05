import { z } from "zod";

export const datasetVisibilitySchema = z.enum(["private", "public"]);
export type DatasetVisibility = z.infer<typeof datasetVisibilitySchema>;

export const artifactRoleSchema = z.enum(["data", "validation"]);
export type ArtifactRole = z.infer<typeof artifactRoleSchema>;

export const profileModeSchema = z.enum(["draft", "released", "archived"]);
export type ProfileMode = z.infer<typeof profileModeSchema>;

export const blockKindSchema = z.enum(["markdown", "inference"]);
export type BlockKind = z.infer<typeof blockKindSchema>;

export const jobRunStatusSchema = z.enum([
	"waiting",
	"running",
	"finished",
	"failed",
]);

export type JobRunStatus = z.infer<typeof jobRunStatusSchema>;

export const availableFunctionSchema = z.enum([
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
]);

export type AvailableFunction = z.infer<typeof availableFunctionSchema>;

export const lossFunctionSchema = z.enum([
	"MSE",
	"Gaussian",
	"Bernoulli",
	"Poisson",
]);

export type LossFunction = z.infer<typeof lossFunctionSchema>;

export const inferenceRunStatusSchema = z.enum([
	"pending",
	"resolving_models",
	"downloading_data",
	"executing",
	"completed",
	"failed",
]);

export type InferenceRunStatus = z.infer<typeof inferenceRunStatusSchema>;
