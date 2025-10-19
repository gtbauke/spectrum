import { Outlet } from "react-router";
import { Sidebar } from "~/components/layout/sidebar.component";

export function SidebarSplitLayout() {
    return (
        <div className="flex h-screen">
            <Sidebar />
            <main className="flex-1 bg-background p-6">
                <Outlet />
            </main>
        </div>
    );
}
