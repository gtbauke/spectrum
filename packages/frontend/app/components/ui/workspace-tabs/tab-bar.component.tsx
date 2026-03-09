export function TabBar() {
    return (
        <div className="flex items-center bg-background-surface border-b border-border h-10 overflow-x-auto no-scrollbar">
            <div className="flex items-center px-4 h-full bg-background border-t-2 border-violet-500 text-sm cursor-pointer group gap-2">
                <span className="text-violet-400">📁</span>
                <span>Production_ETL</span>
                <button
                    type="button"
                    className="ml-3 opacity-0 group-hover:opacity-100 hover:text-red-400"
                >
                    ×
                </button>
            </div>

            <div className="flex items-center px-4 h-full border-r border-border text-sm text-gray-500 hover:bg-white/5 cursor-pointer">
                <span>Staging_Testing</span>
            </div>

            <button
                type="button"
                className="px-3 h-full text-gray-400 hover:text-white hover:bg-white/5 transition"
            >
                +
            </button>
        </div>
    )
}
