import type { Dataset } from "~/schemas/domain/dataset.schema";
import { AddButton } from "../add-button.component";
import { DatasetItem } from "./dataset-item.component";

type ProfileDatasetsSectionProps = {
	datasets: Dataset[];
};

export function ProfileDatasetsSection({
	datasets,
}: ProfileDatasetsSectionProps) {
	return (
		<div className="bg-background-surface border border-border rounded-lg p-4 shadow-sm space-y-2">
			<div className="flex items-center justify-between">
				<h2 className="text-lg font-semibold">Datasets</h2>

				<AddButton
					isEditing={false}
					onEditClick={() => {}}
					onSaveClick={() => {}}
				/>
			</div>
			<div className="space-y-2">
				{datasets.map((dataset) => (
					<DatasetItem key={dataset.id} dataset={dataset} />
				))}
			</div>
		</div>
	);
}
