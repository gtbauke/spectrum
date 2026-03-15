import { z } from "zod";

export const profileDatasetRoleValues = [
	"training",
	"testing",
	"validating",
] as const;
export const profileDatasetRoleSchema = z.enum(profileDatasetRoleValues);

export type ProfileDatasetRole = z.infer<typeof profileDatasetRoleSchema>;
