import { AnimatePresence, motion } from "framer-motion";
import { Undo2, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useEditorStore } from "~/stores/editor.store";

const UNDO_DURATION = 5000; // 5 seconds

export function UndoToast() {
    const lastDeletedBlock = useEditorStore((state) => state.lastDeletedBlock);
    const undoDelete = useEditorStore((state) => state.undoDelete);
    const clearLastDeleted = useEditorStore(
        (state) => state.clearLastDeletedBlock,
    );

    const [progress, setProgress] = useState(100);

    useEffect(() => {
        if (!lastDeletedBlock) return;

        setProgress(100);
        const startTime = Date.now();

        const interval = setInterval(() => {
            const elapsed = Date.now() - startTime;
            const remaining = Math.max(0, 100 - (elapsed / UNDO_DURATION) * 100);
            setProgress(remaining);

            if (remaining === 0) {
                clearLastDeleted();
                clearInterval(interval);
            }
        }, 10);

        return () => clearInterval(interval);
    }, [lastDeletedBlock, clearLastDeleted]);

    return (
        <AnimatePresence>
            {lastDeletedBlock && (
                <motion.div
                    initial={{ y: 100, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: 100, opacity: 0 }}
                    className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 min-w-[320px]"
                >
                    <div className="bg-[#1e2028] border border-white/10 rounded-lg shadow-2xl overflow-hidden">
                        <div className="flex items-center justify-between p-2 gap-6">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-red-500/10 text-red-400 rounded">
                                    <X size={16} />
                                </div>
                                <span className="text-sm text-gray-200 font-medium">
                                    Block deleted
                                </span>
                            </div>

                            <button
                                type="button"
                                onClick={undoDelete}
                                className="flex items-center gap-2 px-3 py-1 bg-primary-500 text-white text-[10px] font-bold rounded hover:bg-primary-600 transition-colors cursor-pointer"
                            >
                                <Undo2 size={12} />
                                Undo
                            </button>
                        </div>

                        <div className="h-1 w-full bg-white/5">
                            <motion.div
                                className="h-full bg-primary-500"
                                initial={{ width: "100%" }}
                                animate={{ width: `${progress}%` }}
                                transition={{ ease: "linear" }}
                            />
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
