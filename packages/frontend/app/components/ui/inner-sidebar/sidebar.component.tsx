import { DatasetExplorer } from "./datasets-explorer-view/sidebar.component";

export function InnerSidebar() {
    return (
        <aside className="w-64 border-r border-border bg-[#111319] flex flex-col">
            <DatasetExplorer />
        </aside>
    );
}
