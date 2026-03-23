import { z } from "zod";
import {
	availableFunctionSchema,
	lossFunctionSchema,
} from "../domain/enums.schema";

export const createJobDtoSchema = z
	.object({
		name: z.string().min(1),
		runsAgainst: z.uuid(),
		generations: z.number().int().default(100),
		population: z.number().int().default(100),
		maxSize: z.number().int().default(40),
		numberOfTournaments: z.number().int().default(4),
		crossoverProbability: z.number().default(0.9),
		mutationProbability: z.number().default(0.1),
		nonTerminals: z.array(availableFunctionSchema).default([]),
		loss: lossFunctionSchema.default("MSE"),
		optimizationIterations: z.number().int().default(0),
		optimizationRepeats: z.number().int().default(1),
		maxParamCount: z.number().int().default(10),
		split: z.number().int().default(75),
		simplify: z.boolean().default(true),
	})
	.transform((data) => ({
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
