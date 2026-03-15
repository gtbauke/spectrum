import { z } from "zod";

export const ownerTypeValues = ["user", "team", "organization"] as const;
export const ownerTypeSchema = z.enum(ownerTypeValues);

export type OwnerType = z.infer<typeof ownerTypeSchema>;
