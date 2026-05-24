import { Import } from "lucide-react";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import { ArtifactItem } from "./artifact-item.component";

type DatasetItemProps = {
	dataset: Dataset;
	canImport?: boolean;
	onImport?: (dataset: Dataset) => void | Promise<void>;
};

export function DatasetItem({
	dataset,
	canImport = false,
	onImport,
}: DatasetItemProps) {
	const handleImport = (e: React.MouseEvent<HTMLButtonElement>) => {
		e.stopPropagation();

		if (onImport) {
			onImport(dataset);
		}
	};

	return (
		<div className="border border-border rounded-md p-2 space-y-2">
			<div className="flex items-start justify-between">
				<div>
					<h3 className="font-bold text-md">{dataset.name}</h3>
					<p className="text-sm text-gray-500">{dataset.description}</p>
				</div>

				{canImport && onImport && (
					<IconButton
						Icon={Import}
						variant="sm"
						className="hover:text-primary-500 hover:bg-primary-500/10"
						onClick={handleImport}
					/>
				)}
			</div>

			<div className="grid grid-cols-2 gap-2">
				{dataset.artifacts.map((artifact) => (
					<ArtifactItem key={artifact.id} artifact={artifact} />
				))}
			</div>
		</div>
	);
}
