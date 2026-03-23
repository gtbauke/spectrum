import { z } from "zod";
import { blockSchema } from "../../../schemas/domain/block.schema";
import type { BulkUpdateBlockDto } from "../../../schemas/dtos/block.dto";
import { safeApiRequest } from "../../fetch.api";

export async function bulkUpdateBlocks(
	profileId: string,
	blocks: BulkUpdateBlockDto[],
) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/blocks`,
		z.array(blockSchema),
		{
			method: "PUT",
			body: JSON.stringify(blocks),
		},
	);

	return response;
}
