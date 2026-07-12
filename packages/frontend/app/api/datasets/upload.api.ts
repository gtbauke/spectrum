import { datasetSchema } from "~/schemas/domain/dataset.schema";
import type { CreateDatasetWithMultipleArtifactsDto } from "~/schemas/dtos/dataset.dto";
import { safeApiRequest } from "../fetch.api";

export async function createDataset(
	files: File[],
	data: CreateDatasetWithMultipleArtifactsDto,
) {
	const formData = new FormData();
	for (const file of files) {
		formData.append("files", file);
	}

	formData.append("name", data.datasetName);
	if (data.datasetDescription) {
		formData.append("description", data.datasetDescription);
	}

	formData.append("roles", JSON.stringify(data.roles));
	formData.append("group_by_columns", JSON.stringify(data.groupByColumns));

	const response = await safeApiRequest("/datasets/upload", datasetSchema, {
		method: "POST",
		body: formData,
	});

	return response;
}
