import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { login, me } from "~/api/auth/auth.api";
import { signup } from "~/api/auth/signup.api";
import type { SignupDto } from "~/schemas/dtos/auth.dto";
import { useAuthStore } from "~/stores/auth.store";

export function useSignupMutation() {
	const setAuth = useAuthStore((s) => s.setAuth);
	const navigate = useNavigate();

	return useMutation({
		mutationFn: async (data: SignupDto) => signup(data),
		onSuccess: async (response, variables) => {
			await login({
				email: response.email,
				password: variables.password,
			});

			const user = await me();

			setAuth(user);
			navigate("/");
		},
	});
}
