import { Filter, Search } from "lucide-react";

type HeaderProps = {
    search: string;
    onSearchChange: (value: string) => void;
};

export function Header({ search, onSearchChange }: HeaderProps) {
    return (
        <div className="p-4 space-y-3 border-b border-border shrink-0">
            <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-widest text-gray-500">
                    Global Search
                </span>
                <button type="button" className="text-gray-500 hover:text-white transition">
                    <Filter size={14} />
                </button>
            </div>

            <div className="relative">
                <Search
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-600"
                    size={14}
                />
                <input
                    type="text"
                    value={search}
                    onChange={(e) => onSearchChange(e.target.value)}
                    placeholder="Search datasets... (⌘K)"
                    className="w-full bg-background border border-border rounded-md pl-9 pr-3 py-2 text-xs outline-none focus:ring-1 focus:ring-primary-500 transition"
                />
            </div>
        </div>
    );
}
