import { z } from "zod";

export const paginationSchema = z.object({
	limit: z.number().int().min(1).default(50),
	offset: z.number().int().min(0).default(0),
});

export type Pagination = z.infer<typeof paginationSchema>;

export function paginatedResponseSchema<T extends z.ZodTypeAny>(itemSchema: T) {
	return z.object({
		items: z.array(itemSchema),
		total: z.number().int(),
		page: z.number().int(),
		size: z.number().int(),
		pages: z.number().int(),
	});
}

export type PaginatedResponse<T> = {
	items: T[];
	total: number;
	page: number;
	size: number;
	pages: number;
};
