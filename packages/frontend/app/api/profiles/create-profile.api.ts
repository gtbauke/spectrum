import { profileSchema } from "~/schemas/domain/profile.schema";
import type { CreateProfileDto } from "~/schemas/dtos/profile.dto";
import { safeApiRequest } from "../fetch.api";

export async function createProfile(data: CreateProfileDto) {
	const response = await safeApiRequest("/profiles", profileSchema, {
		method: "POST",
		body: JSON.stringify(data),
	});

	return response;
}
