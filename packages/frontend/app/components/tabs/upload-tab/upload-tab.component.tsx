import { AlertCircle, CheckCircle2, File, UploadCloud } from "lucide-react";
import Papa from "papaparse";
import { useCallback, useState } from "react";
import { Button } from "~/components/ui/buttons/button.component";
import { DatasetPreviewTable } from "./dataset-preview-table.component";

export default function UploadDatasetTabContent() {
	const [file, setFile] = useState<File | null>(null);
	const [previewData, setPreviewData] = useState<unknown[]>([]);
	const [columns, setColumns] = useState<string[]>([]);
	const [error, setError] = useState<string | null>(null);
	const [isParsing, setIsParsing] = useState(false);
	const [isDragging, setIsDragging] = useState(false);

	const handleFile = useCallback((selectedFile: File) => {
		setError(null);

		if (
			selectedFile.type !== "text/csv" &&
			!selectedFile.name.endsWith(".csv")
		) {
			setError("Please upload a valid CSV file.");
			return;
		}

		setFile(selectedFile);
		setIsParsing(true);

		Papa.parse(selectedFile, {
			header: true,
			dynamicTyping: true,
			skipEmptyLines: true,
			preview: 50,
			complete: (results) => {
				if (results.errors.length > 0) {
					setError(`Parsing error: ${results.errors[0].message}`);
					setIsParsing(false);
					return;
				}

				if (results.data.length > 0) {
					setColumns(Object.keys(results.data[0] as object));
					setPreviewData(results.data);
				}
				setIsParsing(false);
			},
			error: (err) => {
				setError(err.message);
				setIsParsing(false);
			},
		});
	}, []);

	const onDrop = (e: React.DragEvent) => {
		e.preventDefault();
		setIsDragging(false);

		if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
			handleFile(e.dataTransfer.files[0]);
		}
	};

	return (
		<div className="flex flex-col h-screen bg-[#0d0e12] text-gray-200">
			<header className="px-8 py-6 border-b border-white/5 bg-[#111319]">
				<h1 className="text-2xl font-bold text-white">Upload Dataset</h1>
				<p className="text-sm text-gray-400 mt-1">
					Upload a CSV file to create a new dataset model.
				</p>
			</header>

			<div className="flex-1 overflow-y-auto p-8 max-w-7xl mx-auto w-full space-y-8">
				{!file ? (
					// biome-ignore lint/a11y/noStaticElementInteractions: Cannot have nested interactive elements
					<div
						onDragOver={(e) => {
							e.preventDefault();
							setIsDragging(true);
						}}
						onDragLeave={() => setIsDragging(false)}
						onDrop={onDrop}
						className={`flex flex-col items-center justify-center p-16 border-2 border-dashed rounded-xl transition-all ${
							isDragging
								? "border-primary-500 bg-primary-500/10"
								: "border-white/10 bg-[#1e2028] hover:border-white/20 hover:bg-[#252830]"
						}`}
					>
						<UploadCloud size={48} className="text-gray-500 mb-4" />
						<p className="text-lg font-medium text-gray-300">
							Drag & drop your CSV here
						</p>
						<p className="text-sm text-gray-500 mt-2 mb-6">
							or click to browse your files
						</p>

						<label className="cursor-pointer">
							<span className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2.5 rounded-md font-medium transition-colors">
								Browse Files
							</span>
							<input
								type="file"
								accept=".csv"
								className="hidden"
								onChange={(e) =>
									e.target.files && handleFile(e.target.files[0])
								}
							/>
						</label>

						{error && (
							<div className="mt-6 flex items-center gap-2 text-red-400 bg-red-400/10 px-4 py-2 rounded-md">
								<AlertCircle size={16} />
								<span className="text-sm">{error}</span>
							</div>
						)}
					</div>
				) : (
					<div className="flex items-center justify-between p-4 bg-[#1e2028] border border-white/5 rounded-lg">
						<div className="flex items-center gap-4">
							<div className="p-3 bg-green-500/10 rounded-lg">
								<File size={24} className="text-green-500" />
							</div>
							<div>
								<h3 className="font-medium text-white flex items-center gap-2">
									{file.name}
									<CheckCircle2 size={16} className="text-green-500" />
								</h3>
								<p className="text-xs text-gray-500">
									{(file.size / 1024 / 1024).toFixed(2)} MB • CSV Format
								</p>
							</div>
						</div>
						<div className="flex gap-3 ml-auto">
							<Button
								type="button"
								className="bg-transparent border border-white/10 hover:bg-white/5 w-fit px-3"
								onClick={() => {
									setFile(null);
									setPreviewData([]);
								}}
							>
								Cancel
							</Button>
							<Button
								type="button"
								className="w-fit px-3"
								onClick={() => console.log("Upload to backend!", file)}
							>
								Upload Dataset
							</Button>
						</div>
					</div>
				)}

				{file && !isParsing && previewData.length > 0 && (
					<div className="space-y-4">
						<h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider">
							Data Preview (First 50 Rows)
						</h3>
						<DatasetPreviewTable data={previewData} columns={columns} />
					</div>
				)}
			</div>
		</div>
	);
}
