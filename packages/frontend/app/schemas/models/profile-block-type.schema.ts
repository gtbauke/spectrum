import { z } from "zod";

export const profileBlockTypeValues = [
	"inference",
	"markdown",
	"metadata",
	"datasets",
	"jobs",
] as const;
export const profileBlockTypeSchema = z.enum(profileBlockTypeValues);

export type ProfileBlockType = z.infer<typeof profileBlockTypeSchema>;
