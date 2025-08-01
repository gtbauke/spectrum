import { Outlet } from "react-router";
import { Sidebar } from "~/components/layout/sidebar.component";

export function SidebarSplitLayout() {
    return (
        <div className="flex h-screen">
            <Sidebar />
            <main className="p-6 bg-background flex-1">
                <Outlet />
            </main>
        </div>
    );
}
