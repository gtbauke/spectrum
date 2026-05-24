import { profileSchema } from "~/schemas/domain/profile.schema";
import type { LinkDatasetToProfileDto } from "~/schemas/dtos/profile.dto";
import { safeApiRequest } from "../fetch.api";

export async function linkDatasetToProfile(
	profileId: string,
	data: LinkDatasetToProfileDto,
) {
	console.log({
		profileId,
		data,
	});

	const response = await safeApiRequest(
		`/profiles/${profileId}/datasets`,
		profileSchema,
		{
			method: "POST",
			body: JSON.stringify(data),
		},
	);

	return response;
}
