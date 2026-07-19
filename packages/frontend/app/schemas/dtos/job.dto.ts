import { z } from "zod";
import {
	availableFunctionSchema,
	lossFunctionSchema,
} from "../domain/enums.schema";

export const createJobFormSchema = z.object({
	name: z.string().min(1),
	runsAgainst: z.uuid(),
	generations: z.number().int().min(1).default(100),
	population: z.number().int().min(1).default(100),
	maxSize: z.number().int().min(1).default(15),
	numberOfTournaments: z.number().int().min(1).default(3),
	crossoverProbability: z.number().min(0).max(1).default(0.9),
	mutationProbability: z.number().min(0).max(1).default(0.3),
	nonTerminals: z
		.array(availableFunctionSchema)
		.default(["add", "sub", "mul", "div"]),
	loss: lossFunctionSchema.default("MSE"),
	optimizationIterations: z.number().int().min(0).default(50),
	optimizationRepeats: z.number().int().min(1).default(2),
	maxParamCount: z.number().int().min(-1).default(-1),
	split: z.number().int().min(1).default(1),
	simplify: z.boolean().default(false),
	activeGroupByColumns: z.array(z.string()).default([]),
	postProcessingType: z.string().nullable().optional(),
});

export const createJobDtoSchema = createJobFormSchema.transform((data) => ({
	name: data.name,
	runs_against: data.runsAgainst,
	generations: data.generations,
	population: data.population,
	max_size: data.maxSize,
	number_of_tournaments: data.numberOfTournaments,
	crossover_probability: data.crossoverProbability,
	mutation_probability: data.mutationProbability,
	non_terminals: data.nonTerminals,
	loss: data.loss,
	optimization_iterations: data.optimizationIterations,
	optimization_repeats: data.optimizationRepeats,
	max_param_count: data.maxParamCount,
	split: data.split,
	simplify: data.simplify,
	active_group_by_columns: data.activeGroupByColumns,
	post_processing_type: data.postProcessingType,
}));

export type CreateJobDto = z.infer<typeof createJobDtoSchema>;

export const updateJobDtoSchema = z
	.object({
		name: z.string().optional(),
		generations: z.number().int().optional(),
		population: z.number().int().optional(),
		maxSize: z.number().int().optional(),
		numberOfTournaments: z.number().int().optional(),
		crossoverProbability: z.number().optional(),
		mutationProbability: z.number().optional(),
		nonTerminals: z.array(availableFunctionSchema).optional(),
		loss: lossFunctionSchema.optional(),
		optimizationIterations: z.number().int().optional(),
		optimizationRepeats: z.number().int().optional(),
		maxParamCount: z.number().int().optional(),
		split: z.number().int().optional(),
		simplify: z.boolean().optional(),
		activeGroupByColumns: z.array(z.string()).nullable().optional(),
		postProcessingType: z.string().nullable().optional(),
	})
	.transform((data) => ({
		name: data.name,
		generations: data.generations,
		population: data.population,
		max_size: data.maxSize,
		number_of_tournaments: data.numberOfTournaments,
		crossover_probability: data.crossoverProbability,
		mutation_probability: data.mutationProbability,
		non_terminals: data.nonTerminals,
		loss: data.loss,
		optimization_iterations: data.optimizationIterations,
		optimization_repeats: data.optimizationRepeats,
		max_param_count: data.maxParamCount,
		split: data.split,
		simplify: data.simplify,
		active_group_by_columns: data.activeGroupByColumns,
		post_processing_type: data.postProcessingType,
	}));

export type UpdateJobDto = z.infer<typeof updateJobDtoSchema>;

export const bulkUpdateJobDtoSchema = z
	.object({
		id: z.uuid(),
		name: z.string().optional(),
	})
	.transform((data) => ({
		id: data.id,
		name: data.name,
	}));

export type BulkUpdateJobDto = z.infer<typeof bulkUpdateJobDtoSchema>;

export const jobFilterSchema = z.object({
	name: z.string().optional(),
});

export type JobFilter = z.infer<typeof jobFilterSchema>;
