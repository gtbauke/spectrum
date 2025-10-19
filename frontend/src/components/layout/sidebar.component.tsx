import { useEffect, useState } from "react";
import { type Project, parseProjectResponse } from "~/models/project.model";
import { ProjectEntry } from "../project-entry.component";

export function Sidebar() {
    const [projects, setProjects] = useState<Project[]>([]);

    useEffect(() => {
        const _f = async () => {
            const response = await fetch(
                "http://localhost:8000/api/v1/datasets",
            );

            const responseJson = await response.json();
            const projectsFromApi = responseJson.data.map(parseProjectResponse);

            setProjects(projectsFromApi);
        };

        _f();
    }, []);

    return (
        <aside className="min-w-3xs space-y-8 bg-background-secondary p-6">
            <h3 className="font-bold text-lg text-white">My Projects</h3>

            <div className="space-y-4">
                {projects.map((project) => (
                    <ProjectEntry key={project.id} datasetId={project.id}>
                        {project.name}
                    </ProjectEntry>
                ))}
            </div>
        </aside>
    );
}
