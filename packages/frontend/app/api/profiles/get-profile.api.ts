import { profileSchema } from "~/schemas/domain/profile.schema";
import { safeApiRequest } from "../fetch.api";

export async function getProfile(profileId: string) {
	return safeApiRequest(`/profiles/${profileId}`, profileSchema);
}
