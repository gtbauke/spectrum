import { z } from "zod";

export const profileVisibilityValues = ["public", "private"] as const;
export const profileVisibilitySchema = z.enum(profileVisibilityValues);

export type ProfileVisibility = z.infer<typeof profileVisibilitySchema>;
