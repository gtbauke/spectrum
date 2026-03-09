import {
    createContext,
    type PropsWithChildren,
    useCallback,
    useContext,
    useState,
} from "react";

export type ActivityView = "profiles" | "datasets" | "jobs" | "settings" | "account";

export type ActivityContextType = {
    activeView: ActivityView;
    setActiveView: (view: ActivityView) => void;

    isSidebarOpen: boolean;
    setSidebarOpen: (open: boolean) => void;
    toggleSidebar: () => void;
};

const ActivityContext = createContext<ActivityContextType | null>(null);

export function ActivityProvider({ children }: PropsWithChildren) {
    const [activeView, _setActiveView] = useState<ActivityView>("profiles");
    const [isSidebarOpen, setSidebarOpen] = useState(true);

    const setActiveView = useCallback(
        (view: ActivityView) => {
            if (view === activeView && isSidebarOpen) {
                setSidebarOpen(false);
            } else {
                _setActiveView(view);
                setSidebarOpen(true);
            }
        },
        [activeView, isSidebarOpen],
    );

    const toggleSidebar = useCallback(() => {
        setSidebarOpen((open) => !open);
    }, []);

    return (
        <ActivityContext.Provider
            value={{
                activeView,
                setActiveView,
                isSidebarOpen,
                setSidebarOpen,
                toggleSidebar,
            }}
        >
            {children}
        </ActivityContext.Provider>
    );
}

export function useActivity() {
    const context = useContext(ActivityContext);

    if (!context) {
        throw new Error("useActivity must be used within an ActivityProvider");
    }

    return context;
}
