import { type PropsWithChildren, useEffect, useState } from "react";
import { Navigate } from "react-router";
import { apiRequest } from "~/api/fetch.api";
import type { User } from "~/schemas/domain/user.schema";
import { useAuthStore } from "~/stores/auth.store";
import { LoadingScreen } from "../layouts/loading-screen.layout";

type AuthStatus = "loading" | "authenticated" | "unauthenticated";

export function AuthGuard({ children }: PropsWithChildren) {
	const [status, setStatus] = useState<AuthStatus>("loading");

	const setAuth = useAuthStore((state) => state.setAuth);
	const logout = useAuthStore((state) => state.logout);

	useEffect(() => {
		async function checkAuth() {
			try {
				const user = await apiRequest<User>("/auth/me");
				setAuth(user);
				setStatus("authenticated");
			} catch (error) {
				console.error("Session verification failed:", error);
				logout();
				setStatus("unauthenticated");
			}
		}

		checkAuth();
	}, [setAuth, logout]);

	if (status === "loading") {
		return <LoadingScreen />;
	}

	if (status === "unauthenticated") {
		return <Navigate to="/login" replace />;
	}

	return <>{children}</>;
}
