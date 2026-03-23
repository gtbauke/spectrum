import { z } from "zod";
import { safeApiRequest } from "~/api/fetch.api";
import { blockSchema } from "~/schemas/domain/block.schema";
import type { CreateBlockDto } from "~/schemas/dtos/block.dto";

export async function createBlocks(
	profileId: string,
	blocks: CreateBlockDto[],
) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/blocks`,
		z.array(blockSchema),
		{
			method: "POST",
			body: JSON.stringify(blocks),
		},
	);

	return response;
}
