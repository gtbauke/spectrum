import type { Dataset } from "~/schemas/dataset.schema";
import { DatasetCardHeader } from "./header.component";

type DatasetCardProps = {
	dataset: Dataset;
};

export function DatasetCard({ dataset }: DatasetCardProps) {
	return (
		<div className="border rounded p-4 shadow-sm hover:shadow-md transition-shadow space-y-4">
			<DatasetCardHeader
				id={dataset.id}
				name={dataset.name}
				status={dataset.status}
			/>

			<p className="text-xs text-gray-600">{dataset.id}</p>
		</div>
	);
}
