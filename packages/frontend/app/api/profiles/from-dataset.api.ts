import { profileSchema } from "~/schemas/domain/profile.schema";
import type { CreateProfileFromDatasetDto } from "~/schemas/dtos/profile.dto";
import { safeApiRequest } from "../fetch.api";

export async function createProfileFromDataset(
	file: File,
	data: CreateProfileFromDatasetDto,
) {
	const formData = new FormData();
	formData.append("file", file);

	formData.append("dataset_name", data.datasetName);
	if (data.datasetDescription) {
		formData.append("dataset_description", data.datasetDescription);
	}

	formData.append("dataset_role", data.datasetRole);

	const response = await safeApiRequest(
		"/profiles/from-dataset",
		profileSchema,
		{
			method: "POST",
			body: formData,
		},
	);

	return response;
}
