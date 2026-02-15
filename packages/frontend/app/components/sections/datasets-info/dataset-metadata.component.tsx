import { Section } from "~/components/ui/section.component";
import type { DatasetMetadata as DatasetMetadataType } from "~/schemas/dataset.schema";

type DatasetMetadataProps = {
	metadata: DatasetMetadataType | null | undefined;
};

export function DatasetMetadata({ metadata }: DatasetMetadataProps) {
	if (!metadata) {
		return (
			<Section title="Metadata">
				<p className="text-sm text-gray-500">
					No metadata available yet for this dataset.
				</p>
			</Section>
		);
	}

	return (
		<Section title="Metadata">
			<div className="space-y-1">
				<p>Number of rows: {metadata.num_rows}</p>
				<p>Number of features: {metadata.num_features}</p>
				<p>Processing attempts: {metadata.processing_attempts}</p>
				{metadata.last_processing_error && (
					<p className="text-red-500">
						Last processing error: {metadata.last_processing_error}
					</p>
				)}
			</div>
		</Section>
	);
}
