import { apiRequest } from "../../fetch.api";

export async function deleteBlock(profileId: string, blockId: string) {
	await apiRequest(`/profiles/${profileId}/blocks/${blockId}`, {
		method: "DELETE",
	});
}
