import { z } from "zod";

export const paginatedResponseSchema = <T extends z.ZodType>(itemSchema: T) =>
	z.object({
		items: z.array(itemSchema),
		total: z.int().nonnegative(),
		page: z.int().nonnegative(),
		size: z.int().nonnegative(),
		pages: z.int().nonnegative(),
	});

export type PaginatedResponse<T> = {
	items: T[];
	total: number;
	page: number;
	size: number;
	pages: number;
};
