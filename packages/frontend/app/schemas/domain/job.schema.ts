import { z } from "zod";
import { baseMutableObject, baseVersionedObject } from "../common/base.schema";
import {
	availableFunctionSchema,
	jobRunStatusSchema,
	lossFunctionSchema,
} from "./enums.schema";

export const runSchema = baseVersionedObject
	.extend({
		job_id: z.uuid(),
		status: jobRunStatusSchema,
		started_at: z.coerce.date().nullable(),
		finished_at: z.coerce.date().nullable(),
	})
	.transform((data) => ({
		id: data.id,
		version: data.version,
		jobId: data.job_id,
		status: data.status,
		startedAt: data.started_at,
		finishedAt: data.finished_at,
		timestamp: data.timestamp,
		isLatest: data.is_latest,
	}));

export type Run = z.infer<typeof runSchema>;

export const jobSchema = baseMutableObject
	.extend({
		name: z.string(),
		profile_id: z.uuid(),
		runs_against: z.uuid(),
		generations: z.number().int(),
		population: z.number().int(),
		max_size: z.number().int(),
		number_of_tournaments: z.number().int(),
		crossover_probability: z.number(),
		mutation_probability: z.number(),
		non_terminals: z.array(availableFunctionSchema),
		loss: lossFunctionSchema,
		optimization_iterations: z.number().int(),
		optimization_repeats: z.number().int(),
		max_param_count: z.number().int(),
		split: z.number().int(),
		simplify: z.boolean(),
		runs: z.array(runSchema),
	})
	.transform((data) => ({
		id: data.id,
		name: data.name,
		profileId: data.profile_id,
		runsAgainst: data.runs_against,
		generations: data.generations,
		population: data.population,
		maxSize: data.max_size,
		numberOfTournaments: data.number_of_tournaments,
		crossoverProbability: data.crossover_probability,
		mutationProbability: data.mutation_probability,
		nonTerminals: data.non_terminals,
		loss: data.loss,
		optimizationIterations: data.optimization_iterations,
		optimizationRepeats: data.optimization_repeats,
		maxParamCount: data.max_param_count,
		split: data.split,
		simplify: data.simplify,
		runs: data.runs.map((run) => (run.jobId ? run : runSchema.parse(run))),
		createdAt: data.created_at,
		updatedAt: data.updated_at,
	}));

export type Job = z.infer<typeof jobSchema>;
