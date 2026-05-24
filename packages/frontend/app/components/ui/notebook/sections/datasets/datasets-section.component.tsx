import { useState } from "react";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import { AddButton } from "../add-button.component";
import { AddDataset } from "./add-dataset.component";
import { DatasetItem } from "./dataset-item.component";

type ProfileDatasetsSectionProps = {
	datasets: Dataset[];
	profileId: string;
};

export function ProfileDatasetsSection({
	datasets,
	profileId,
}: ProfileDatasetsSectionProps) {
	const [isAdding, setIsAdding] = useState(false);

	const handleAddClick = () => {
		setIsAdding(true);
	};

	const handleSaveClick = () => {
		setIsAdding(false);
	};

	const handleCancelClick = () => {
		setIsAdding(false);
	};

	return (
		<div className="bg-background-surface border border-border rounded-lg p-4 shadow-sm space-y-2">
			<div className="flex items-center justify-between">
				<h2 className="text-lg font-semibold">Datasets</h2>

				<AddButton
					isEditing={isAdding}
					onEditClick={handleAddClick}
					onSaveClick={handleSaveClick}
					onCancelClick={handleCancelClick}
				/>
			</div>

			{isAdding && (
				<AddDataset existingDatasets={datasets} profileId={profileId} />
			)}

			<div className="space-y-2">
				{datasets.map((dataset) => (
					<DatasetItem key={dataset.id} dataset={dataset} />
				))}
			</div>
		</div>
	);
}
