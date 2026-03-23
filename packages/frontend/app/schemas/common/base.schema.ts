import { z } from "zod";

export const baseMutableObject = z.object({
	id: z.uuid(),
	created_at: z.coerce.date(),
	updated_at: z.coerce.date(),
});

export const baseMutableSchema = baseMutableObject.transform((data) => ({
	id: data.id,
	createdAt: data.created_at,
	updatedAt: data.updated_at,
}));

export const baseImmutableObject = z.object({
	id: z.uuid(),
	timestamp: z.coerce.date(),
});

export const baseImmutableSchema = baseImmutableObject.transform((data) => ({
	id: data.id,
	timestamp: data.timestamp,
}));

export const baseVersionedObject = z.object({
	id: z.uuid(),
	version: z.number().int(),
	timestamp: z.coerce.date(),
	is_latest: z.boolean(),
});

export const baseVersionedSchema = baseVersionedObject.transform((data) => ({
	id: data.id,
	version: data.version,
	timestamp: data.timestamp,
	isLatest: data.is_latest,
}));

export type BaseMutable = z.infer<typeof baseMutableSchema>;
export type BaseImmutable = z.infer<typeof baseImmutableSchema>;
export type BaseVersioned = z.infer<typeof baseVersionedSchema>;
