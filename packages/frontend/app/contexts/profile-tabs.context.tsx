import {
    createContext,
    type PropsWithChildren,
    useCallback,
    useContext,
    useState,
} from "react";
import type { ProfileVersion } from "~/schemas/generated/profile-version.schema";

export type ProfileTab = {
    id: string;
    name: string;
    isDirty?: boolean;

    profileId: string;
    profileVersion: ProfileVersion;
};

export type ProfileTabsContextType = {
    tabs: ProfileTab[];
    activeTabId: string | null;

    openTab: (profileTab: ProfileTab) => void;
    closeTab: (id: string) => void;
    setActiveTab: (id: string) => void;

    updateTab: (id: string, updates: Partial<ProfileTab>) => void;
};

const ProfileTabsContext = createContext<ProfileTabsContextType | null>(null);

export function ProfileTabsProvider({ children }: PropsWithChildren) {
    const [tabs, setTabs] = useState<ProfileTab[]>([]);
    const [activeTabId, setActiveTabId] = useState<string | null>(null);

    const openTab = useCallback((profileTab: ProfileTab) => {
        setTabs((prevTabs) => {
            const existingTab = prevTabs.find((tab) => tab.id === profileTab.id);

            if (existingTab) {
                return prevTabs;
            }

            return [...prevTabs, profileTab];
        });
        setActiveTabId(profileTab.id);
    }, []);

    const closeTab = useCallback(
        (id: string) => {
            setTabs((prev) => {
                const newTabs = prev.filter((tab) => tab.id !== id);

                if (activeTabId === id) {
                    const closedIndex = prev.findIndex((tab) => tab.id === id);
                    const nextTab = newTabs[closedIndex - 1] || newTabs[0];

                    setActiveTabId(nextTab ? nextTab.id : null);
                }

                return newTabs;
            });
        },
        [activeTabId],
    );

    const updateTab = useCallback((id: string, updates: Partial<ProfileTab>) => {
        setTabs(prev => prev.map(tab => tab.id === id ? { ...tab, ...updates } : tab));
    }, []);

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
