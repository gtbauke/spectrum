import { Suspense, useEffect, useState } from "react";
import { useParams } from "react-router";
import { JobEntry } from "~/components/job-entry.component";
import { type Project, parseProjectResponse } from "~/models/project.model";

type DatasetPageParams = {
    datasetId: string;
};

export function DatasetPage() {
    const { datasetId } = useParams<DatasetPageParams>();
    const [dataset, setDataset] = useState<Project>();

    useEffect(() => {
        const _f = async () => {
            const response = await fetch(
                `http://localhost:8000/api/v1/datasets/${datasetId}`,
            );
            const responseJson = await response.json();
            const parsedResponse = parseProjectResponse(responseJson.data);
            setDataset(parsedResponse);
        };

        _f();
    }, [datasetId]);

    return (
        <Suspense fallback={<p>Loading...</p>}>
            <div className="space-y-4">
                <h1 className="text-white">
                    Dataset {dataset?.name} - {datasetId}
                </h1>

                <div className="space-y-2">
                    {dataset?.jobs.map((job) => (
                        <JobEntry
                            key={job.id}
                            id={job.id}
                            name={job.description}
                        />
                    ))}
                </div>
            </div>
        </Suspense>
    );
}
