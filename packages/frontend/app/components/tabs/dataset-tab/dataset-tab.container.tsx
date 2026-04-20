import {
	ChevronLeft,
	ChevronRight,
	Database,
	FileDigit,
	FileText,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useArtifactPreview } from "~/hooks/use-artifact-preview.hook";
import { useDataset } from "~/hooks/use-dataset.hook";
import { useDatasetUpdateMutation } from "~/hooks/use-dataset-update-mutation.hook";
import { formatBytes } from "~/utils/format-bytes.util";
import { DatasetPreviewTable } from "../upload-tab/dataset-preview-table.component";

type DatasetTabContainerProps = {
	datasetId: string;
};

export function DatasetTabContainer({ datasetId }: DatasetTabContainerProps) {
	const { data: dataset, isLoading } = useDataset(datasetId);
	const updateDataset = useDatasetUpdateMutation();

	const [isEditingName, setIsEditingName] = useState(false);
	const [name, setName] = useState("");

	const [isEditingDesc, setIsEditingDesc] = useState(false);
	const [description, setDescription] = useState("");

	const [activeArtifactId, setActiveArtifactId] = useState<string | null>(null);
	const [limit, setLimit] = useState(50);
	const [offset, setOffset] = useState(0);

	const { data: preview, isLoading: isPreviewLoading } = useArtifactPreview(
		datasetId,
		activeArtifactId,
		limit,
		offset,
	);

	useEffect(() => {
		if (dataset) {
			setName(dataset.name);
			setDescription(dataset.description || "");

			if (
				!activeArtifactId &&
				dataset.artifacts &&
				dataset.artifacts.length > 0
			) {
				setActiveArtifactId(dataset.artifacts[0].id);
			}
		}
	}, [dataset, activeArtifactId]);

	const handleUpdate = () => {
		if (
			dataset &&
			(name !== dataset.name || description !== (dataset.description || ""))
		) {
			updateDataset.mutate({
				datasetId,
				data: { name, description },
			});
		}
	};

	if (isLoading) {
		return (
			<div className="flex flex-col h-screen bg-[#0d0e12] text-gray-200">
				<header className="px-8 py-6 border-b border-white/5 bg-[#111319]">
					<div className="w-64 h-8 bg-white/10 animate-pulse mb-2 rounded" />
					<div className="w-96 h-4 bg-white/10 animate-pulse rounded" />
				</header>
			</div>
		);
	}

	return (
		<div className="flex flex-col h-screen bg-[#0d0e12] text-gray-200 overflow-hidden">
			<header className="px-8 py-6 border-b border-white/5 bg-[#111319] shrink-0">
				<div className="flex flex-col gap-1">
					{isEditingName ? (
						<input
							type="text"
							value={name}
							onChange={(e) => setName(e.target.value)}
							onBlur={() => {
								setIsEditingName(false);
								handleUpdate();
							}}
							onKeyDown={(e) => {
								if (e.key === "Enter") e.currentTarget.blur();
							}}
							className="text-2xl font-bold text-white bg-[#1e2028] border border-primary/30 rounded px-2 py-1 outline-none focus:border-primary transition-colors"
						/>
					) : (
						<h1
							className="text-2xl font-bold text-white cursor-text hover:text-gray-300 transition-colors w-fit px-2 py-1 -ml-2 rounded border border-transparent hover:border-white/10"
							onClick={() => setIsEditingName(true)}
							onKeyDown={(e) => {
								if (e.key === "Enter") {
									e.currentTarget.blur();
								}
							}}
						>
							{name || "Untitled Dataset"}
						</h1>
					)}

					{isEditingDesc ? (
						<textarea
							value={description}
							onChange={(e) => setDescription(e.target.value)}
							onBlur={() => {
								setIsEditingDesc(false);
								handleUpdate();
							}}
							onKeyDown={(e) => {
								if (e.key === "Enter" && !e.shiftKey) {
									e.preventDefault();
									e.currentTarget.blur();
								}
							}}
							className="text-sm text-gray-300 bg-[#1e2028] border border-primary/30 rounded px-2 py-1 outline-none focus:border-primary transition-colors w-full max-w-2xl resize-none h-20"
						/>
					) : (
						<p
							className="text-sm text-gray-400 cursor-text hover:text-gray-300 transition-colors w-full max-w-2xl px-2 py-1 -ml-2 rounded border border-transparent hover:border-white/10"
							onClick={() => setIsEditingDesc(true)}
							onKeyDown={(e) => {
								if (e.key === "Enter") {
									e.currentTarget.blur();
								}
							}}
						>
							{description || "Add a description..."}
						</p>
					)}
				</div>
			</header>

			<div className="flex flex-1 overflow-hidden">
				{/* Left Main Area: Preview */}
				<div className="flex-1 flex flex-col min-w-0 bg-[#0d0e12] relative">
					{activeArtifactId ? (
						<div className="flex flex-col h-full">
							<div className="px-6 py-4 flex items-center justify-between border-b border-white/5 shrink-0">
								<h2 className="text-sm font-medium text-gray-300 flex items-center gap-2">
									<Database className="w-4 h-4 text-emerald-500" />
									Data Preview
								</h2>
								{preview && (
									<div className="text-xs text-gray-500">
										Showing rows {offset + 1}-
										{Math.min(offset + limit, preview.total)} of {preview.total}
									</div>
								)}
							</div>

							<div className="flex-1 overflow-auto p-6">
								{isPreviewLoading ? (
									<div className="flex items-center justify-center h-full">
										<div className="w-8 h-8 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
									</div>
								) : preview ? (
									<div className="h-full flex flex-col">
										<div className="flex-1 min-h-0">
											<DatasetPreviewTable
												columns={preview.columns}
												data={preview.data}
											/>
										</div>

										{/* Pagination */}
										<div className="flex items-center justify-between pt-4 mt-auto shrink-0">
											<div className="flex items-center gap-2">
												<span className="text-xs text-gray-500">Limit</span>
												<select
													className="bg-[#1e2028] border border-white/10 rounded text-xs px-2 py-1 text-gray-300 outline-none"
													value={limit}
													onChange={(e) => {
														setLimit(Number(e.target.value));
														setOffset(0);
													}}
												>
													<option value={10}>10</option>
													<option value={50}>50</option>
													<option value={100}>100</option>
													<option value={500}>500</option>
												</select>
											</div>

											<div className="flex gap-2">
												<button
													type="button"
													className={`flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded transition-colors ${
														offset === 0
															? "bg-white/5 text-gray-600 cursor-not-allowed"
															: "bg-[#1e2028] text-gray-300 hover:bg-white/10 hover:text-white border border-white/10"
													}`}
													disabled={offset === 0}
													onClick={() => setOffset(Math.max(0, offset - limit))}
												>
													<ChevronLeft className="w-3 h-3" /> Prev
												</button>
												<button
													type="button"
													className={`flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded transition-colors ${
														!preview || offset + limit >= preview.total
															? "bg-white/5 text-gray-600 cursor-not-allowed"
															: "bg-[#1e2028] text-gray-300 hover:bg-white/10 hover:text-white border border-white/10"
													}`}
													disabled={!preview || offset + limit >= preview.total}
													onClick={() => setOffset(offset + limit)}
												>
													Next <ChevronRight className="w-3 h-3" />
												</button>
											</div>
										</div>
									</div>
								) : (
									<div className="flex flex-col items-center justify-center h-full text-center">
										<div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-4">
											<FileDigit className="w-6 h-6 text-gray-500" />
										</div>
										<h3 className="text-sm font-medium text-gray-300 mb-1">
											Unable to load preview
										</h3>
										<p className="text-xs text-gray-500 max-w-62.5">
											There was a problem loading the data sample for this
											artifact. Ensure it is a valid CSV file.
										</p>
									</div>
								)}
							</div>
						</div>
					) : (
						<div className="flex items-center justify-center h-full text-gray-500 text-sm">
							Select an artifact to preview its contents.
						</div>
					)}
				</div>

				{/* Right Sidebar: Artifact List */}
				<div className="w-64 shrink-0 border-l border-white/5 bg-[#111319] flex flex-col">
					<div className="p-4 border-b border-white/5">
						<h3 className="text-xs font-bold uppercase tracking-wider text-gray-400">
							Associated Artifacts
						</h3>
					</div>
					<div className="flex-1 overflow-y-auto p-4 space-y-2">
						{dataset?.artifacts?.map((artifact) => (
							// biome-ignore lint/a11y/useSemanticElements: Cannot have nested interactive elements
							<div
								role="button"
								tabIndex={0}
								key={artifact.id}
								onClick={() => {
									setActiveArtifactId(artifact.id);
									setOffset(0);
								}}
								onKeyDown={(e) => {
									if (e.key === "Enter") {
										setActiveArtifactId(artifact.id);
										setOffset(0);
									}
								}}
								className={`p-3 rounded-lg border cursor-pointer transition-all ${
									activeArtifactId === artifact.id
										? "bg-primary/10 border-primary/40 ring-1 ring-primary/20"
										: "bg-white/2 border-white/5 hover:bg-white/5 hover:border-white/10"
								}`}
							>
								<div className="flex items-start gap-3">
									<div
										className={`mt-0.5 ${activeArtifactId === artifact.id ? "text-primary" : "text-gray-500"}`}
									>
										<FileText className="w-4 h-4" />
									</div>
									<div className="flex flex-col min-w-0">
										<span
											className={`text-sm truncate font-medium ${activeArtifactId === artifact.id ? "text-white" : "text-gray-300"}`}
										>
											{artifact.path.split("/").pop()}
										</span>
										<div className="flex items-center gap-2 mt-1">
											<span className="text-[10px] text-gray-500 uppercase tracking-widest font-mono">
												{artifact.role}
											</span>
											<span className="w-1 h-1 rounded-full bg-white/10" />
											<span className="text-[10px] text-gray-500">
												{formatBytes(artifact.sizeInBytes)}
											</span>
										</div>
									</div>
								</div>
							</div>
						))}

						{(!dataset?.artifacts || dataset.artifacts.length === 0) && (
							<div className="text-center py-8">
								<p className="text-xs text-gray-500">No artifacts found.</p>
							</div>
						)}
					</div>
				</div>
			</div>
		</div>
	);
}
