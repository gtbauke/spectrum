import { z } from "zod";
import { profileSummarySchema } from "~/schemas/domain/profile.schema";
import { safeApiRequest } from "../fetch.api";

export async function listProfileSummaries() {
	const response = await safeApiRequest(
		"/profiles/summary",
		z.array(profileSummarySchema),
	);

	return response;
}
