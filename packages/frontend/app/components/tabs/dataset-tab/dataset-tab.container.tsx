import { useDataset } from "~/hooks/use-dataset.hook";
import { DatasetPreviewTable } from "../upload-tab/dataset-preview-table.component";

type DatasetTabContainerProps = {
	datasetId: string;
};

export function DatasetTabContainer({ datasetId }: DatasetTabContainerProps) {
	const { data: dataset, isLoading } = useDataset(datasetId);

	if (isLoading) {
		return (
			<div className="flex flex-col h-screen bg-[#0d0e12] text-gray-200">
				<header className="px-8 py-6 border-b border-white/5 bg-[#111319]">
					<div className="w-full h-px bg-white/10 animate-pulse" />
					<div className="w-full h-px bg-white/10 animate-pulse" />
				</header>

				<div className="flex-1 overflow-y-auto p-8 max-w-7xl mx-auto w-full space-y-8">
					<div className="w-full h-6 bg-white/10 animate-pulse mb-4" />
				</div>
			</div>
		);
	}

	return (
		<div className="flex flex-col h-screen bg-[#0d0e12] text-gray-200">
			<header className="px-8 py-6 border-b border-white/5 bg-[#111319]">
				<h1 className="text-2xl font-bold text-white">{dataset?.name}</h1>
				<p className="text-sm text-gray-400 mt-1">
					{dataset?.description || "No description provided."}
				</p>
			</header>

			<div className="flex-1 overflow-y-auto p-8 max-w-7xl mx-auto w-full space-y-8"></div>
		</div>
	);
}
