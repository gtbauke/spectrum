import { useParams } from "react-router";

type DatasetPageParams = {
    datasetId: string;
};

export function DatasetPage() {
    const { datasetId } = useParams<DatasetPageParams>();

    return (
        <div>
            <h1 className="text-white">Dataset - {datasetId}</h1>
        </div>
    );
}
