import { userSchema } from "~/schemas/domain/user.schema";
import type { SignupDto } from "~/schemas/dtos/auth.dto";
import { safeApiRequest } from "../fetch.api";

export async function signup(data: SignupDto) {
	const response = await safeApiRequest("/users", userSchema, {
		method: "POST",
		body: JSON.stringify(data),
	});

	return response;
}
