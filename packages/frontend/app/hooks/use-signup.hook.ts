import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { authApi } from "~/api/auth.api";
import type { SignupInput } from "~/schemas/signup.schema";
import { useAuthStore } from "~/stores/auth.store";

export function useSignupMutation() {
	const setAuth = useAuthStore((s) => s.setAuth);
	const navigate = useNavigate();

	return useMutation({
		mutationFn: (data: SignupInput) => authApi.signup(data),
		onSuccess: async (response, variables) => {
			const loginResponse = await authApi.login({
				email: response.email,
				password: variables.password,
			});

			localStorage.setItem("access_token", loginResponse.access_token);
			setAuth(loginResponse.user);

			navigate("/");
		},
	});
}
