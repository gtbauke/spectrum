import { index, type RouteConfig, route } from "@react-router/dev/routes";

export default [
	index("routes/home.tsx"),
	route("/datasets/create", "routes/dataset-creation.tsx"),
	route("/datasets", "routes/datasets.tsx"),
	route("/datasets/:datasetId/jobs", "routes/jobs.tsx"),
	route("/playground/:modelId", "routes/playground.tsx"),
] satisfies RouteConfig;
