import { zodResolver } from "@hookform/resolvers/zod";
import { AlertCircle } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useCreateProfileFromDatasetMutation } from "~/hooks/use-create-profile-from-dataset.hook";
import { createDatasetWithMultipleArtifactsSchema } from "~/schemas/dtos/dataset.dto";
import { DatasetPreviewTable } from "./dataset-preview-table.component";
import { EditDatasetForm } from "./edit-dataset-form.component";
import { useFileUpload } from "./file-upload.context";
import { UploadFileContainer } from "./upload-file-container.component";

export default function UploadDatasetTabContent() {
	const [isDragging, setIsDragging] = useState(false);
	const { files, reset: resetUploads, selectedFileName } = useFileUpload();

	const hasFiles = Object.keys(files).length > 0;

	const { formState, register, handleSubmit, reset } = useForm({
		resolver: zodResolver(createDatasetWithMultipleArtifactsSchema),
		defaultValues: {
			datasetName: "",
			datasetDescription: "",
			roles: Object.entries(files).map(([fileName]) => ({
				fileName,
				role: undefined,
			})),
		},
	});

	const {
		mutate,
		isPending,
		error: mutationError,
	} = useCreateProfileFromDatasetMutation();

	const handleUpload = handleSubmit((data) => {
		console.log("Form Data:", data);
		console.log("Files:", files);

		const filesArray = Object.values(files);
		if (filesArray.length === 0) {
			return;
		}

		// mutate({
		// 	file,
		// 	data: data as CreateProfileFromDatasetDto,
		// });
	});

	const handleCancel = () => {
		reset();
		resetUploads();
	};

	const shouldShowPreview =
		selectedFileName && !files[selectedFileName].isParsing;
	const previewData = shouldShowPreview
		? files[selectedFileName]?.previewData
		: [];
	const columns = shouldShowPreview ? files[selectedFileName]?.columns : [];

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

				{!hasFiles ? (
					<UploadFileContainer
						isDragging={isDragging}
						setIsDragging={setIsDragging}
					/>
				) : (
					<EditDatasetForm
						register={register}
						isPending={isPending}
						handleUpload={handleUpload}
						handleCancel={handleCancel}
						isValid={formState.isValid}
					/>
				)}

				{shouldShowPreview &&
					previewData &&
					columns &&
					previewData.length > 0 && (
						<div className="space-y-4">
							<h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider">
								Data Preview for {selectedFileName} (First 50 Rows)
							</h3>

							<DatasetPreviewTable data={previewData} columns={columns} />
						</div>
					)}
			</div>
		</div>
	);
}
