import { Plus } from "lucide-react";
import type { ProfileDatasetAssociation } from "~/schemas/generated/profile-dataset-association.schema";

type DatasetsCellProps = {
	datasets: ProfileDatasetAssociation[];
};

export function DatasetsBlock({ datasets }: DatasetsCellProps) {
	if (!datasets?.length) {
		return null;
	}

	return (
		<div className="space-y-2">
			<span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
				Attached Datasets
			</span>
			<div className="rounded border border-white/5 overflow-hidden">
				{datasets?.map((ds) => (
					<div
						key={ds.id}
						className="flex justify-between items-center p-3 border-b border-white/5 bg-[#111319]/50 hover:bg-white/5 transition-colors text-sm text-gray-300"
					>
						<span>{ds.dataset_version?.name || "Dataset"}</span>
						<span className="text-[10px] uppercase bg-primary-500/10 text-primary-400 px-2 py-0.5 rounded">
							{ds.role}
						</span>
					</div>
				))}
				{datasets?.length === 0 && (
					<div className="p-4 text-center text-xs text-gray-500">
						No datasets attached.
					</div>
				)}
			</div>
			<button
				type="button"
				className="text-xs text-primary-400 hover:text-primary-300 flex items-center gap-1 mt-2"
			>
				<Plus size={12} /> Add Dataset
			</button>
		</div>
	);
}
