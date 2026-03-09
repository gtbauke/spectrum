import { WorkspaceLayout } from "~/components/layouts/workspace.layout";
import type { Route } from "./+types/home";

export function meta(_: Route.MetaArgs) {
    return [
        { title: "Spectrum" },
        {
            name: "description",
            content: "The web platform for Symbolic Regression",
        },
    ];
}

export default function Home() {
    return (
        <WorkspaceLayout />
    );
}
