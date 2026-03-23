import { apiRequest } from "../fetch.api";

export async function deleteProfile(profileId: string) {
	await apiRequest(`/profiles/${profileId}`, {
		method: "DELETE",
	});
}
