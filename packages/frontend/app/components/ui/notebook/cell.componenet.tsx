import { GripVertical, MoreHorizontal, Play, Trash2 } from "lucide-react";
import { useState } from "react";
import { cn } from "~/utils/classname.util";

type CellType = "markdown" | "dataset" | "configuration" | "results";

type NotebookCellProps = {
    id: string;
    type: CellType;
    isActive: boolean;
    onClick: () => void;
    children: React.ReactNode;
    onRun?: () => void;
};

export function NotebookCell({
    id,
    type,
    isActive,
    onClick,
    children,
    onRun,
}: NotebookCellProps) {
    const [isHovered, setIsHovered] = useState(false);

    const handleOnKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
        if (e.key === "Enter") {
            onClick();
        }
    };

    return (
        // biome-ignore lint/a11y/noStaticElementInteractions: Cannot have nested buttons
        <div
            className="group relative flex w-full max-w-4xl mx-auto mb-2"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            onKeyDown={handleOnKeyDown}
            onClick={onClick}
        >
            {/* The Left Action Gutter */}
            <div
                className={cn(
                    "w-12 shrink-0 flex flex-col items-center pt-3 transition-opacity duration-200",
                    isHovered || isActive ? "opacity-100" : "opacity-0",
                )}
            >
                {/* Drag Handle */}
                <button
                    type="button"
                    className="p-1 text-gray-600 hover:text-gray-300 cursor-grab"
                >
                    <GripVertical size={16} />
                </button>

                {/* Execution/Run Button (if applicable) */}
                {onRun && (
                    <button
                        type="button"
                        onClick={(e) => {
                            e.stopPropagation();
                            onRun();
                        }}
                        className="mt-1 p-1.5 rounded-full bg-white/5 text-gray-400 hover:bg-emerald-500/20 hover:text-emerald-400 transition-colors"
                        title="Run cell"
                    >
                        <Play size={14} className="ml-0.5" />
                    </button>
                )}
            </div>

            {/* The Main Cell Content */}
            <div
                className={cn(
                    "flex-1 relative rounded-lg border transition-all duration-200 bg-black/20",
                    isActive
                        ? "border-purple-500/50 shadow-[0_0_0_1px_rgba(168,85,247,0.2)]"
                        : "border-white/5 hover:border-white/10",
                )}
            >
                {/* Optional: Cell Type Indicator */}
                {(isHovered || isActive) && (
                    <div className="absolute -top-2.5 right-4 px-2 py-0.5 bg-[#111319] border border-white/10 rounded text-[9px] font-mono text-gray-500 uppercase tracking-wider z-10">
                        {type}
                    </div>
                )}

                <div className="p-4 outline-none">{children}</div>
            </div>

            {/* The Right Action Gutter (Delete, Options) */}
            <div
                className={cn(
                    "w-10 shrink-0 flex flex-col items-center pt-3 transition-opacity duration-200",
                    isHovered || isActive ? "opacity-100" : "opacity-0",
                )}
            >
                <button
                    type="button"
                    className="p-1.5 text-gray-600 hover:text-red-400 transition-colors"
                >
                    <Trash2 size={14} />
                </button>
                <button
                    type="button"
                    className="mt-1 p-1.5 text-gray-600 hover:text-gray-300 transition-colors"
                >
                    <MoreHorizontal size={14} />
                </button>
            </div>
        </div>
    );
}
