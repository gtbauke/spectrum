export type JobApiResponse = {
    id: string;
    dataset_id: string;
    description: string;

    generations: number;
    max_optimization_restarts: number;
    population_size: number;
    parameter_count: number;
    max_expression_size: number;
    split: number;
    tournament_size: number;
    crossover_probability: number;
    mutation_probability: number;
    max_optimization_iterations: number;
    simplify: boolean;

    loss_function: string;
    fileName: string;

    created_at: Date;
    updated_at: Date;
};

export type Job = {
    id: string;
    datasetId: string;
    description: string;

    generations: number;
    maxOptimizationRestarts: number;
    populationSize: number;
    parameterCount: number;
    maxExpressionSize: number;
    split: number;
    tournamentSize: number;
    crossoverProbability: number;
    mutationProbability: number;
    maxOptimizationIterations: number;
    simplify: boolean;

    lossFunction: string;
    fileName: string;

    createdAt: Date;
    updatedAt: Date;
};

export type ProjectApiResponse = {
    id: string;
    name: string;
    description: string;
    dataset_file_path: string;

    created_at: Date;
    updated_at: Date;

    jobs: JobApiResponse[];
};

export type Project = {
    id: string;
    name: string;
    description: string;
    datasetFilePath: string;

    createdAt: Date;
    updatedAt: Date;

    jobs: Job[];
};

export function parseJobResponse(jobApiResponse: JobApiResponse): Job {
    return {
        id: jobApiResponse.id,
        datasetId: jobApiResponse.dataset_id,
        description: jobApiResponse.description,

        generations: jobApiResponse.generations,
        maxOptimizationRestarts: jobApiResponse.max_optimization_restarts,
        populationSize: jobApiResponse.population_size,
        parameterCount: jobApiResponse.parameter_count,
        maxExpressionSize: jobApiResponse.max_expression_size,
        split: jobApiResponse.split,
        tournamentSize: jobApiResponse.tournament_size,
        crossoverProbability: jobApiResponse.crossover_probability,
        mutationProbability: jobApiResponse.mutation_probability,
        maxOptimizationIterations: jobApiResponse.max_optimization_iterations,
        simplify: jobApiResponse.simplify,

        lossFunction: jobApiResponse.loss_function,
        fileName: jobApiResponse.fileName,

        createdAt: jobApiResponse.created_at,
        updatedAt: jobApiResponse.updated_at,
    };
}

export function parseProjectResponse(
    projectApiResponse: ProjectApiResponse,
): Project {
    return {
        id: projectApiResponse.id,
        name: projectApiResponse.name,
        description: projectApiResponse.description,
        datasetFilePath: projectApiResponse.dataset_file_path,

        createdAt: projectApiResponse.created_at,
        updatedAt: projectApiResponse.updated_at,

        jobs: projectApiResponse.jobs.map(parseJobResponse),
    };
}
