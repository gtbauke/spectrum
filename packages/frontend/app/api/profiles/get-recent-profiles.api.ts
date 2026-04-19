import { z } from "zod";
import { profileSchema } from "~/schemas/domain/profile.schema";
import { safeApiRequest } from "../fetch.api";

export async function getRecentProfiles() {
	return safeApiRequest(`/profiles/recent`, z.array(profileSchema));
}
