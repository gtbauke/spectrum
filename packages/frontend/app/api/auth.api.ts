import type { User } from "~/schemas/generated/user.schema";
import type { LoginInput } from "~/schemas/login.schema";
import type { SignupInput } from "~/schemas/signup.schema";
import { apiRequest } from "./fetch.api";

export const authApi = {
	login: async (credentials: LoginInput) => {
		const data = await apiRequest<{ access_token: string; user: User }>(
			"/auth/login",
			{
				method: "POST",
				body: JSON.stringify(credentials),
			},
		);

		localStorage.setItem("access_token", data.access_token);
		return data;
	},

	logout: async () => {
		await apiRequest("/auth/logout", { method: "POST" });
		localStorage.removeItem("access_token");

		window.location.href = "/login";
	},

	signup: async (data: SignupInput) => {
		const response = await apiRequest<User>("/users", {
			method: "POST",
			body: JSON.stringify(data),
		});

		return response;
	},
};
