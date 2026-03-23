import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { login } from "~/api/auth/auth.api";
import type { LoginCredentials } from "~/schemas/dtos/auth.dto";
import { useAuthStore } from "~/stores/auth.store";

export function useLoginMutation() {
	const setAuth = useAuthStore((s) => s.setAuth);
	const navigate = useNavigate();

	return useMutation({
		mutationFn: (data: LoginCredentials) => login(data),
		onSuccess: async (response: any) => {
			setAuth(response.user);
			navigate("/");
		},
	});
}
