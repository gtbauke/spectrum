import { AlertCircle, UploadCloud } from "lucide-react";
import Papa from "papaparse";
import { useCallback } from "react";
import { useFileUpload } from "./file-upload.context";

type UploadFileContainerProps = {
	isDragging: boolean;
	setIsDragging: (isDragging: boolean) => void;
};

export function UploadFileContainer({
	isDragging,
	setIsDragging,
}: UploadFileContainerProps) {
	const { addFiles, setError, setErrors, updateFile, files } = useFileUpload();
	const allErrors = Object.values(files).flatMap((f) =>
		f.error ? [f.error] : [],
	);

	const handleFiles = useCallback(
		(files: FileList) => {
			setErrors({});

			if (files.length === 0) {
				return;
			}

			for (const file of files) {
				if (file.type !== "text/csv" && !file.name.endsWith(".csv")) {
					setError(file.name, "Invalid file type. Please upload a CSV file.");
				}
			}

			addFiles(Array.from(files));

			for (const file of files) {
				updateFile(file.name, { isParsing: true });

				Papa.parse(file, {
					header: true,
					dynamicTyping: true,
					skipEmptyLines: true,
					preview: 50,
					complete: (results) => {
						if (results.errors.length > 0) {
							setError(
								file.name,
								`Parsing error: ${results.errors[0].message}`,
							);

							updateFile(file.name, { isParsing: false });
							return;
						}

						const columns =
							results.data.length > 0
								? Object.keys(results.data[0] as object)
								: [];

						updateFile(file.name, {
							columns,
							previewData: results.data,
							isParsing: false,
						});
					},
					error: (err) => {
						setError(file.name, err.message);
						updateFile(file.name, { isParsing: false });
					},
				});
			}
		},
		[addFiles, setError, setErrors, updateFile],
	);

	const onDrop = useCallback(
		(e: React.DragEvent) => {
			e.preventDefault();
			setIsDragging(false);

			if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
				handleFiles(e.dataTransfer.files);
			}
		},
		[handleFiles, setIsDragging],
	);

	return (
		// biome-ignore lint/a11y/noStaticElementInteractions: Needs to handle drag and drop events on a div
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
					multiple
					onChange={(e) => e.target.files && handleFiles(e.target.files)}
				/>
			</label>

			{allErrors.map((error, idx) => (
				<div
					key={`${error}-${idx.toString()}`}
					className="mt-6 flex items-center gap-2 text-red-400 bg-red-400/10 px-4 py-2 rounded-md"
				>
					<AlertCircle size={16} />
					<span className="text-sm">{error}</span>
				</div>
			))}
		</div>
	);
}
