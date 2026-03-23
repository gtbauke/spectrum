import { z } from "zod";

export const loginCredentialsSchema = z.object({
	email: z.email(),
	password: z.string().min(8),
});

export type LoginCredentials = z.infer<typeof loginCredentialsSchema>;

export const signupDtoSchema = z.object({
	first_name: z.string().min(1),
	last_name: z.string().min(1),
	email: z.email(),
	password: z.string().min(8),
});

export type SignupDto = z.infer<typeof signupDtoSchema>;
