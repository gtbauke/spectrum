import { z } from "zod";
import { ownerTypeSchema } from "~/schemas/models/owner-type.schema";
import { userDetailsSchema } from "../users/user-details.schema";

export const ownerDetailsSchema = z.object({
	id: z.uuid(),
	type: ownerTypeSchema,
	details: userDetailsSchema,
});

export type OwnerDetailsApiPayload = z.input<typeof ownerDetailsSchema>;
export type OwnerDetails = z.infer<typeof ownerDetailsSchema>;
