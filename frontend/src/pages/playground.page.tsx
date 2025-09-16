import { useParams } from "react-router";

type PlaygroundPageParams = {
    datasetId: string;
};

export function PlaygroundPage() {
    const { datasetId } = useParams<PlaygroundPageParams>();

    return (
        <div>
            <h1>Playground</h1>
            <p>Dataset: {datasetId}</p>

            <div>
                <label className="flex flex-col gap-2">
                    Query
                    <input className="border border-white p-2" />
                </label>
            </div>
        </div>
    );
}
