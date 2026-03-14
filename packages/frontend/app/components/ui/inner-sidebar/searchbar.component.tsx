import { Search } from "lucide-react";

type SidebarSearchInputProps = {
    search: string;
    onSearchChange: (value: string) => void;
} & React.InputHTMLAttributes<HTMLInputElement>;

export function SidebarSearchInput({ search, onSearchChange, ...props }: SidebarSearchInputProps) {
    return (
        <div className="relative">
            <Search
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-600"
                size={14}
            />
            <input
                {...props}
                value={search}
                onChange={(e) => onSearchChange(e.target.value)}
                className="w-full bg-background border border-border rounded-md pl-9 pr-3 py-2 text-xs outline-none focus:ring-1 focus:ring-primary-500 transition"
            />
        </div>
    )
}
