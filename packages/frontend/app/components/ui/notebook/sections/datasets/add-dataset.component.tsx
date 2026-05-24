import { Button } from "~/components/ui/buttons/button.component";
import { useDatasets } from "~/hooks/use-datasets.hook";
import { useLinkDatasetToProfileMutation } from "~/hooks/use-link-dataset-to-profile-mutation.hook";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import { useEditorStore } from "~/stores/editor.store";
import { DatasetItem } from "./dataset-item.component";

type AddDatasetProps = {
	existingDatasets: Dataset[];
	profileId: string;
};

export function AddDataset({ existingDatasets, profileId }: AddDatasetProps) {
	const { data: datasets, isLoading } = useDatasets();
	const { mutate: linkDatasetToProfile } = useLinkDatasetToProfileMutation();
	const openUploadTab = useEditorStore((s) => s.openUploadTab);

	const handleDatasetImportClick = async (dataset: Dataset) => {
		linkDatasetToProfile({
			profile: {
				id: profileId,
			},
			data: {
				dataset_ids: [dataset.id],
			},
		});
	};

	if (isLoading) {
		return <div>Loading...</div>;
	}

	return (
		<div className="p-4 border border-border rounded-lg bg-background-surface space-y-4">
			<div className="space-y-4">
				<div className="space-y-2">
					<h3 className="text-md font-medium">New Dataset</h3>
					<Button className="text-sm" onClick={openUploadTab}>
						Add New Dataset
					</Button>
				</div>

				<div className="space-y-2">
					<h3 className="text-md font-medium">Existing Datasets</h3>

					{!datasets || datasets?.items?.length === 0 ? (
						<p className="text-sm text-gray-500">No datasets found.</p>
					) : (
						<ul className="space-y-3">
							{datasets.items
								.filter((d) => !existingDatasets.find((ed) => ed.id === d.id))
								.map((dataset) => (
									<li key={dataset.id}>
										<DatasetItem
											dataset={dataset}
											canImport
											onImport={handleDatasetImportClick}
										/>
									</li>
								))}
						</ul>
					)}
				</div>
			</div>
		</div>
	);
}
