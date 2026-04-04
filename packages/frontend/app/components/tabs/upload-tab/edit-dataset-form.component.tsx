import { Eye, File, Trash2 } from "lucide-react";
import type { UseFormRegister } from "react-hook-form";
import { Button } from "~/components/ui/buttons/button.component";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import { Field } from "~/components/ui/forms/field/field.component";
import { SelectInput } from "~/components/ui/forms/input/select-input.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import {
	type ArtifactRole,
	artifactRoleSchema,
} from "~/schemas/domain/enums.schema";
import { capitalize } from "~/utils/capitalize.util";
import { useFileUpload } from "./file-upload.context";

type EditDatasetFormProps = {
	handleUpload: (e: React.BaseSyntheticEvent | undefined) => void;
	handleCancel: () => void;
	register: UseFormRegister<{
		datasetName: string;
		datasetDescription?: string;
		roles: {
			fileName: string;
			role?: ArtifactRole;
		}[];
	}>;
	isValid: boolean;
	isPending: boolean;
};

export function EditDatasetForm({
	handleUpload,
	handleCancel,
	register,
	isValid,
	isPending,
}: EditDatasetFormProps) {
	const { files, removeFile, selectFile } = useFileUpload();

	const fileEntries = Object.entries(files);
	const filesCount = fileEntries.length;

	const fileErrors = fileEntries.reduce(
		(acc, [fileName, file]) => {
			if (file.error) acc[fileName] = file.error;
			return acc;
		},
		{} as Record<string, string>,
	);

	const onFilePreview = (fileName: string) => {
		selectFile(fileName);
	};

	return (
		<form
			onSubmit={handleUpload}
			className="flex flex-col gap-6 p-6 bg-[#1e2028] border border-white/5 rounded-lg"
		>
			<div className="space-y-4 pb-6 border-b border-white/5">
				<div className="flex items-center gap-3 mb-2">
					<div className="p-2 bg-blue-500/10 rounded-lg">
						<File size={20} className="text-blue-500" />
					</div>
					<h3 className="text-sm font-bold text-gray-200 uppercase tracking-wider">
						Dataset Details
					</h3>
				</div>

				<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div className="space-y-2">
						<Field>
							<Field.Label required>Dataset Name</Field.Label>
							<Field.Control>
								<TextInput
									placeholder="e.g., Q3 Marketing Data"
									{...register("datasetName")}
									disabled={isPending}
								/>
							</Field.Control>
						</Field>
					</div>

					<Field>
						<Field.Label>Description</Field.Label>
						<Field.Control>
							<TextAreaInput
								placeholder="Brief context about this data batch..."
								{...register("datasetDescription")}
								disabled={isPending}
								className="min-h-24"
							/>
						</Field.Control>
					</Field>
				</div>
			</div>

			<div className="space-y-4">
				<div className="flex items-center justify-between">
					<h3 className="text-sm font-bold text-gray-200 uppercase tracking-wider">
						Artifact Roles ({filesCount})
					</h3>
				</div>

				<div className="flex flex-col gap-3 max-h-80 overflow-y-auto pr-2 custom-scrollbar">
					{filesCount === 0 ? (
						<p className="text-sm text-gray-500 italic">No files selected.</p>
					) : (
						fileEntries.map(([fileName, fileData], index) => (
							<div
								key={fileName}
								className="flex items-center justify-between p-4 bg-white/5 border border-white/10 rounded-lg gap-4"
							>
								<div className="flex items-center gap-3 overflow-hidden flex-1">
									<div className="p-2 bg-green-500/10 rounded-md shrink-0">
										<File size={20} className="text-green-500" />
									</div>
									<div className="flex flex-col min-w-0">
										<span
											className="text-sm font-medium text-white truncate"
											title={fileName}
										>
											{fileName}
										</span>
										<span className="text-xs text-gray-500">
											{(fileData.file.size / 1024 / 1024).toFixed(2)} MB
										</span>
										{fileErrors[fileName] && (
											<span className="text-xs text-red-500 mt-0.5">
												{fileErrors[fileName]}
											</span>
										)}
									</div>
								</div>

								<input
									type="hidden"
									value={fileName}
									{...register(`roles.${index}.fileName` as const)}
								/>

								<div className="w-48 shrink-0">
									<Field>
										<Field.Label required>Role</Field.Label>
										<Field.Control>
											<SelectInput
												aria-label={`Role for ${fileName}`}
												{...register(`roles.${index}.role`, { required: true })}
												disabled={isPending}
												options={artifactRoleSchema.options.map((value) => ({
													label: capitalize(value),
													value,
												}))}
											/>
										</Field.Control>
									</Field>
								</div>

								<IconButton
									Icon={Trash2}
									aria-label={`Remove ${fileName}`}
									onClick={() => removeFile(fileName)}
									disabled={isPending}
									className="p-2 text-gray-500 hover:bg-red-500/10 hover:text-red-400 transition-colors shrink-0"
								/>

								<IconButton
									Icon={Eye}
									aria-label={`Preview ${fileName}`}
									onClick={() => onFilePreview(fileName)}
									disabled={isPending}
									className="p-2 text-gray-500 hover:bg-blue-500/10 hover:text-blue-400 transition-colors shrink-0"
								/>
							</div>
						))
					)}
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
					disabled={isPending || filesCount === 0 || !isValid}
				>
					Upload & Create
				</Button>
			</div>
		</form>
	);
}
