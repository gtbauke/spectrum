import type { PropsWithChildren } from "react";
import { useActivity } from "~/contexts/activity-view.context";
import { useKeyboardShortcut } from "~/hooks/use-keyboard-shortcut.hook";
import { ActivitySidebar } from "../ui/activity-sidebar/sidebar.component";
import { InnerSidebar } from "../ui/inner-sidebar/sidebar.component";
import { TabBar } from "../ui/workspace-tabs/tab-bar.component";

type WorkspaceLayoutProps = PropsWithChildren;

export function WorkspaceLayout({ children }: WorkspaceLayoutProps) {
    const { isSidebarOpen, toggleSidebar, setActiveView } = useActivity();

    useKeyboardShortcut("b", toggleSidebar);

    useKeyboardShortcut("1", () => setActiveView("profiles"));
    useKeyboardShortcut("2", () => setActiveView("datasets"));
    useKeyboardShortcut("3", () => setActiveView("jobs"));

    useKeyboardShortcut(",", () => setActiveView("settings"));

    return (
        <div className="flex h-screen flex-col bg-background text-white">
            <div className="flex flex-1 overflow-hidden">
                <ActivitySidebar />

                {isSidebarOpen && <InnerSidebar />}

                <div className="flex-1 flex flex-col overflow-hidden">
                    <TabBar />
                    <main className="flex-1 relative bg-[radial-gradient(#2D3343_1px,transparent_1px)] bg-size-[24px_24px] overflow-auto">
                        {children}
                    </main>
                </div>
            </div>
        </div>
    );
}
