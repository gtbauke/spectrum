import { Database, FileText, MoreVertical } from "lucide-react";
import { cn } from "~/utils/classname.util";

type DatasetItemProps = {
    name: string;
    type: string;
    size: string;
    active?: boolean;
};

export function DatasetItem({
    name,
    type,
    size,
    active = false,
}: DatasetItemProps) {
    return (
        <div
            className={cn(
                "group flex items-center justify-between p-2 rounded-md cursor-pointer transition-colors",
                active
                    ? "bg-primary-500/10 text-white"
                    : "text-gray-400 hover:bg-white/5 hover:text-gray-200",
            )}
        >
            <div className="flex items-center gap-3 truncate">
                {type === "SQL" ? (
                    <Database size={14} className="text-blue-400" />
                ) : (
                    <FileText size={14} className="text-orange-400" />
                )}
                <div className="flex flex-col truncate">
                    <span className="text-xs font-medium truncate">{name}</span>
                    <span className="text-[10px] text-gray-600">
                        {size} • {type}
                    </span>
                </div>
            </div>

            <button
                type="button"
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white/10 rounded transition-all"
            >
                <MoreVertical size={14} />
            </button>
        </div>
    );
}
