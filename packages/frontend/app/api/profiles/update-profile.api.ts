import { profileSchema } from "../../schemas/domain/profile.schema";
import type { UpdateProfileDto } from "../../schemas/dtos/profile.dto";
import { safeApiRequest } from "../fetch.api";

export async function updateProfile(profileId: string, data: UpdateProfileDto) {
	const response = await safeApiRequest(
		`/profiles/${profileId}`,
		profileSchema,
		{
			method: "PUT",
			body: JSON.stringify(data),
		},
	);

	return response;
}
