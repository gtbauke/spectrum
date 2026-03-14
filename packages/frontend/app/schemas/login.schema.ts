import { z } from "zod";

export const loginSchema = z.object({
	email: z.email().min(1),
	password: z
		.string()
		.min(8, "Password must be at least 8 characters long")
		.regex(/[a-z]/, "Password must contain at least one lowercase letter")
		.regex(/[A-Z]/, "Password must contain at least one uppercase letter")
		.regex(/[0-9]/, "Password must contain at least one digit")
		.regex(
			/[@$!%*?&]/,
			"Password must contain at least one special character (@$!%*?&)",
		),
});

export type LoginInput = z.infer<typeof loginSchema>;
