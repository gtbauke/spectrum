import type { z } from "zod";

export function validateEnum<T extends z.ZodEnum>(
	value: string,
	schema: T,
): z.infer<T> {
	const res = schema.safeParse(value);

	if (!res.success) {
		throw new Error("Invalid enum value");
	}

	return res.data;
}
