import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";
import { cn } from "~/utils/classname.util";

type ToolbarButtonProps = {
    icon: React.ReactNode;
    label: string;
    shortcut?: string;
    onClick: () => void;
    disabled?: boolean;
    className?: string;
};

export function ToolbarButton({
    icon,
    label,
    shortcut,
    onClick,
    disabled = false,
    className,
}: ToolbarButtonProps) {
    const [isHovered, setIsHovered] = useState(false);

    return (
        <div className="relative flex items-center justify-center">
            <button
                type="button"
                disabled={disabled}
                onClick={onClick}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className={cn(
                    "p-2 rounded-md transition-all outline-none focus-visible:ring-1 focus-visible:ring-primary-500",
                    disabled
                        ? "opacity-30 cursor-not-allowed"
                        : "text-gray-400 hover:text-white hover:bg-white/5 active:scale-95",
                    className,
                )}
            >
                {icon}
            </button>

            <AnimatePresence>
                {isHovered && !disabled && (
                    <motion.div
                        initial={{ opacity: 0, y: 5, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        transition={{ duration: 0.1 }}
                        className="absolute top-full mt-2 z-50 pointer-events-none"
                    >
                        <div className="bg-[#2a2d38] border border-white/10 rounded px-2 py-1 shadow-2xl flex items-center gap-3 whitespace-nowrap">
                            <span className="text-[10px] font-bold text-gray-200 uppercase tracking-tight">
                                {label}
                            </span>
                            {shortcut && (
                                <span className="text-[9px] font-mono text-gray-500 bg-black/30 px-1 rounded border border-white/5">
                                    {shortcut}
                                </span>
                            )}
                        </div>

                        <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-[#2a2d38] border-l border-t border-white/10 rotate-45" />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
