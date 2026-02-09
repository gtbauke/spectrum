import { zodResolver } from "@hookform/resolvers/zod";

import { useCallback } from "react";
import { type SubmitHandler, useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { createDataset } from "~/api/create-dataset.api";
import { FormInput } from "~/components/ui/forms/form-input.component";
import { useDatasetCreationContext } from "~/contexts/dataset-creation.context";
import {
	type CreateDatasetData,
	createDatasetSchema,
} from "~/schemas/dataset.schema";

export function DatasetsAsideSection() {
	const { file } = useDatasetCreationContext();
	const navigate = useNavigate();

	const {
		register,
		handleSubmit,
		reset,
		formState: { errors },
	} = useForm<CreateDatasetData>({
		defaultValues: {
			name: file?.originalName || "",
		},
		resolver: zodResolver(createDatasetSchema),
	});

	const onCancel = useCallback(() => {
		reset();
		navigate("/");
	}, [reset, navigate]);

	const onSubmit: SubmitHandler<CreateDatasetData> = async (data) => {
		console.log(errors);
		console.log(data);

		if (!file || !file.upload) {
			console.error("No file provided for dataset creation");
			return;
		}

		try {
			const response = await createDataset(data, file.upload);
			console.log("Dataset created successfully:", response);

			navigate("/datasets");
		} catch (error) {
			console.error("Error creating dataset:", error);
		}
	};

	return (
		<div className="h-full bg-gray-900 p-4 space-y-8">
			<h2 className="text-xl font-bold">Configure your dataset</h2>

			<form
				className="flex flex-col gap-3"
				onSubmit={handleSubmit(onSubmit)}
				onReset={onCancel}
			>
				<FormInput
					label="Dataset name"
					error={errors.name}
					required
					{...register("name", { required: true })}
				/>

				<div className="flex flex-col gap-2">
					<input
						type="submit"
						value="Continue"
						className="cursor-pointer p-2 bg-green-600 hover:bg-green-700 active:bg-green-800 rounded-sm font-bold"
					/>

					<input
						type="reset"
						value="Cancel"
						className="cursor-pointer p-2 bg-red-600 hover:bg-red-700 active:bg-red-800 rounded-sm font-bold"
					/>
				</div>
			</form>
		</div>
	);
}
