import { safeApiRequest } from "~/api/fetch.api";
import { blockSchema } from "~/schemas/domain/block.schema";
import type { UpdateBlockDto } from "~/schemas/dtos/block.dto";

export async function updateBlock(
	profileId: string,
	blockId: string,
	data: UpdateBlockDto,
) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/blocks/${blockId}`,
		blockSchema,
		{
			method: "PUT",
			body: JSON.stringify(data),
		},
	);

	return response;
}
