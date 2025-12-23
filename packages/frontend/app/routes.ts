import { index, type RouteConfig, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("/datasets", "routes/dataset-creation.tsx"),
] satisfies RouteConfig;
