import { zodResolver } from "@hookform/resolvers/zod";
import { AlertCircle, CheckCircle2, File, UploadCloud } from "lucide-react";
import Papa from "papaparse";
import { useCallback, useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "~/components/ui/buttons/button.component";
import { SelectInput } from "~/components/ui/forms/input/select-input.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { useCreateProfileFromDatasetMutation } from "~/hooks/use-create-profile-from-dataset.hook";
import { createProfileFromDatasetSchema } from "~/schemas/create-profile-from-dataset.schema";
import { profileDatasetRoleValues } from "~/schemas/models/profile-dataset-role.schema";
import { capitalize } from "~/utils/capitalize.util";
import { DatasetPreviewTable } from "./dataset-preview-table.component";

export default function UploadDatasetTabContent() {
	const [file, setFile] = useState<File | null>(null);
	const [previewData, setPreviewData] = useState<unknown[]>([]);
	const [columns, setColumns] = useState<string[]>([]);
	const [error, setError] = useState<string | null>(null);
	const [isParsing, setIsParsing] = useState(false);
	const [isDragging, setIsDragging] = useState(false);

	const {
		formState: { errors, isValid },
		register,
		handleSubmit,
		reset,
	} = useForm({
		resolver: zodResolver(createProfileFromDatasetSchema),
		defaultValues: {
			datasetName: "",
			datasetDescription: "",
			datasetRole: "training",
		},
	});

	const {
		mutate,
		isPending,
		error: mutationError,
	} = useCreateProfileFromDatasetMutation();

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

	const handleUpload = handleSubmit((data) => {
		console.log(data);

		if (!file) {
			return;
		}

		mutate({
			file,
			datasetName: data.datasetName,
			datasetDescription: data.datasetDescription || "",
			datasetRole: data.datasetRole,
		});
	});

	const handleCancel = () => {
		setFile(null);
		setPreviewData([]);
		setError(null);
		reset();
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
				{mutationError && (
					<div className="flex items-center gap-2 text-red-400 bg-red-400/10 px-4 py-3 rounded-md border border-red-500/20">
						<AlertCircle size={18} />
						<span className="text-sm font-medium">{mutationError.message}</span>
					</div>
				)}

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
					<form
						onSubmit={handleUpload}
						className="flex flex-col gap-6 p-6 bg-[#1e2028] border border-white/5 rounded-lg"
					>
						<div className="flex items-center justify-between pb-6 border-b border-white/5">
							<div className="flex items-center gap-4">
								<div className="p-3 bg-green-500/10 rounded-lg">
									<File size={24} className="text-green-500" />
								</div>
								<div>
									<h3 className="font-medium text-white flex items-center gap-2">
										{file.name}
										<CheckCircle2 size={16} className="text-green-500" />
									</h3>
									<p className="text-xs text-gray-500 mt-1">
										{(file.size / 1024 / 1024).toFixed(2)} MB • CSV Format
									</p>
								</div>
							</div>
						</div>

						<div className="space-y-4">
							<h3 className="text-sm font-bold text-gray-200 uppercase tracking-wider">
								Dataset Details
							</h3>
							<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
								<div className="space-y-2">
									<TextInput
										label="Dataset Name"
										required
										placeholder="e.g., Q3 Marketing Data"
										{...register("datasetName", {
											required: "Dataset name is required",
										})}
										error={errors.datasetName}
										disabled={isPending}
									/>

									<SelectInput
										label="Dataset Role"
										required
										{...register("datasetRole", {
											required: "Dataset role is required",
										})}
										error={errors.datasetRole}
										disabled={isPending}
										options={profileDatasetRoleValues.map((value) => ({
											label: capitalize(value),
											value,
										}))}
									/>
								</div>

								<TextAreaInput
									label="Description"
									placeholder="Brief context about this data..."
									{...register("datasetDescription")}
									error={errors.datasetDescription}
									disabled={isPending}
									className="min-h-35"
								/>
							</div>
						</div>

						<div className="flex gap-3 pt-4 justify-end border-t border-white/5 mt-2">
							<Button
								type="button"
								className="bg-transparent border border-white/10 hover:bg-white/5 w-fit px-4"
								onClick={handleCancel}
								disabled={isPending}
							>
								Cancel
							</Button>
							<Button
								type="submit"
								className="w-fit px-6"
								isLoading={isPending}
								disabled={isPending || !file || !isValid}
							>
								Upload & Create
							</Button>
						</div>
					</form>
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
