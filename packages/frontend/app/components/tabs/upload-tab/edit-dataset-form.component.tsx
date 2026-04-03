import { CheckCircle2, File } from "lucide-react";
import type { UseFormRegister } from "react-hook-form";
import { Button } from "~/components/ui/buttons/button.component";
import { SelectInput } from "~/components/ui/forms/input/select-input.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { artifactRoleSchema } from "~/schemas/domain/enums.schema";
import { capitalize } from "~/utils/capitalize.util";
import { useFileUpload } from "./file-upload.context";
import { SelectFileDropdown } from "./select-file-dropdown.component";

type EditDatasetFormProps = {
	handleUpload: (e: React.BaseSyntheticEvent | undefined) => void;
	handleCancel: () => void;
	register: UseFormRegister<{
		datasetName: string;
		datasetDescription?: string | undefined;
		datasetRole?: "data" | "validation" | undefined;
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
	const { files } = useFileUpload();
	const errors = Object.entries(files).reduce(
		(acc, [fileName, file]) => {
			if (file.error) {
				acc[fileName] = file.error;
			}

			return acc;
		},
		{} as Record<string, string>,
	);

	return (
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
						<SelectFileDropdown />
						{/* <h3 className="font-medium text-white flex items-center gap-2">
							{files[0].file.name}
							<CheckCircle2 size={16} className="text-green-500" />
						</h3>
						<p className="text-xs text-gray-500 mt-1">
							{(files[0].file.size / 1024 / 1024).toFixed(2)} MB • CSV Format
							Test
						</p> */}
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
							{...register("datasetName")}
							error={errors.datasetName}
							disabled={isPending}
						/>

						<SelectInput
							label="Dataset Role"
							required
							{...register("datasetRole")}
							error={errors.datasetRole}
							disabled={isPending}
							options={artifactRoleSchema.options.map((value) => ({
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
					disabled={isPending || !files || !isValid}
				>
					Upload & Create
				</Button>
			</div>
		</form>
	);
}
