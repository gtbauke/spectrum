import type { Dataset } from "~/schemas/domain/dataset.schema";
import { ArtifactItem } from "./artifact-item.component";

type DatasetItemProps = {
	dataset: Dataset;
};

export function DatasetItem({ dataset }: DatasetItemProps) {
	return (
		<div className="border border-border rounded-md p-2 space-y-2">
			<div>
				<h3 className="font-bold text-md">{dataset.name}</h3>
				<p className="text-sm text-gray-500">{dataset.description}</p>
			</div>

			<div className="grid grid-cols-2 gap-2">
				{dataset.artifacts.map((artifact) => (
					<ArtifactItem key={artifact.id} artifact={artifact} />
				))}
			</div>
		</div>
	);
}
