import {
	createContext,
	type PropsWithChildren,
	useCallback,
	useContext,
	useState,
} from "react";
import type { ProfileVersion } from "~/schemas/models/profile-version.schema";

export type ProfileTab = {
	type: "profile";

	id: string;
	name: string;
	isDirty?: boolean;

	profileId: string;
	profileVersion: ProfileVersion;
};

export type UploadTab = {
	type: "upload";

	id: string;
	name: string;
};

export type Tab = ProfileTab | UploadTab;

type TabTypeMap = {
	profile: ProfileTab;
	upload: UploadTab;
};

export type ProfileTabsContextType = {
	tabs: Tab[];
	activeTabId: string | null;

	openTab: (tab: Tab) => void;
	closeTab: (id: string) => string | null;
	setActiveTab: (id: string) => void;

	updateTab: <T extends Tab["type"]>(
		id: string,
		type: T,
		updates: Partial<Omit<TabTypeMap[T], "id" | "type">>,
	) => void;
};

const ProfileTabsContext = createContext<ProfileTabsContextType | null>(null);

export function ProfileTabsProvider({ children }: PropsWithChildren) {
	const [tabs, setTabs] = useState<Tab[]>([]);
	const [activeTabId, setActiveTabId] = useState<string | null>(null);

	const openTab = useCallback((tab: Tab) => {
		setTabs((prevTabs) => {
			const existingTab = prevTabs.find((t) => t.id === tab.id);

			if (existingTab) {
				return prevTabs;
			}

			return [...prevTabs, tab];
		});

		setActiveTabId(tab.id);
	}, []);

	const closeTab = useCallback(
		(id: string) => {
			const newTabs = tabs.filter((tab) => tab.id !== id);

			if (activeTabId === id) {
				const closedIndex = tabs.findIndex((tab) => tab.id === id);
				const nextTab = newTabs[closedIndex - 1] || newTabs[0];

				setActiveTabId(nextTab?.id ?? null);
				setTabs(newTabs);

				return nextTab.id;
			}

			return null;
		},
		[activeTabId, tabs],
	);

	const updateTab = useCallback(
		<T extends Tab["type"]>(
			id: string,
			type: T,
			updates: Partial<Omit<TabTypeMap[T], "id" | "type">>,
		) => {
			setTabs((prev) =>
				prev.map((tab) => {
					if (tab.id === id && tab.type === type) {
						return { ...tab, ...updates } as Tab;
					}
					return tab;
				}),
			);
		},
		[],
	);

	return (
		<ProfileTabsContext.Provider
			value={{
				tabs,
				activeTabId,
				openTab,
				closeTab,
				setActiveTab: setActiveTabId,
				updateTab,
			}}
		>
			{children}
		</ProfileTabsContext.Provider>
	);
}

export function useProfileTabs() {
	const context = useContext(ProfileTabsContext);

	if (!context) {
		throw new Error("useProfileTabs must be used within a ProfileTabsProvider");
	}

	return context;
}
