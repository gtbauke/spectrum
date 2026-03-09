export function InnerSidebar() {
    return (
        <aside className="w-64 border-r border-border bg-[#111319] flex flex-col">
            <div className="p-4 uppercase text-[10px] font-bold tracking-widest text-gray-500">
                Datasets
            </div>
            <div className="flex-1 overflow-y-auto px-2 space-y-1">
                <div className="flex items-center p-2 rounded hover:bg-white/5 text-sm cursor-pointer gap-2">
                    <span className="text-blue-400">📊</span> user_behavior_v1
                </div>
            </div>

            <button
                type="button"
                className="m-4 p-2 border border-dashed border-border rounded text-xs text-gray-500 hover:border-violet-500 hover:text-violet-400 transition"
            >
                + New Dataset
            </button>
        </aside>
    );
}
