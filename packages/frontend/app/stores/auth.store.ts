import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { User } from "~/schemas/domain/user.schema";

type AuthState = {
	user: User | null;
	isAuthenticated: boolean;

	setAuth: (user: User) => void;
	logout: () => void;
};

export const useAuthStore = create<AuthState>()(
	persist(
		(set) => ({
			user: null,
			isAuthenticated: false,

			setAuth: (user) => {
				set({ user, isAuthenticated: !!user });
			},
			logout: () => {
				localStorage.removeItem("access_token");
				set({ user: null, isAuthenticated: false });
			},
		}),
		{
			name: "auth-storage",
			storage: createJSONStorage(() =>
				typeof window !== "undefined" ? localStorage : dummyStorage,
			),
		},
	),
);

const dummyStorage = {
	getItem: () => null,
	setItem: () => undefined,
	removeItem: () => undefined,
};
