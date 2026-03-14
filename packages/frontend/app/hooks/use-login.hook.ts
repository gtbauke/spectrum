import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { authApi } from "~/api/auth.api";
import type { LoginInput } from "~/schemas/login.schema";
import { useAuthStore } from "~/stores/auth.store";

export function useLoginMutation() {
	const setAuth = useAuthStore((s) => s.setAuth);
	const navigate = useNavigate();

	return useMutation({
		mutationFn: (data: LoginInput) => authApi.login(data),
		onSuccess: async (response) => {
			setAuth(response.user);
			navigate("/");
		},
	});
}
