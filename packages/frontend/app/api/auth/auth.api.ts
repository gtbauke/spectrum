import { userSchema } from "~/schemas/domain/user.schema";
import type { LoginCredentials } from "~/schemas/dtos/auth.dto";
import { apiRequest, safeApiRequest } from "../fetch.api";

export async function login(credentials: LoginCredentials) {
	return apiRequest("/auth/login", {
		method: "POST",
		body: JSON.stringify(credentials),
	});
}

export async function logout() {
	await apiRequest("/auth/logout", { method: "POST" });
}

export async function me() {
	return safeApiRequest("/auth/me", userSchema);
}
