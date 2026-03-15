import { z } from "zod";

export const profileStatusValues = ["active", "inactive", "deleted"] as const;
export const profileStatusSchema = z.enum(profileStatusValues);

export type ProfileStatus = z.infer<typeof profileStatusSchema>;
