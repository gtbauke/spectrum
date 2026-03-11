import { AnimatePresence, motion } from "framer-motion";
import {
    ChevronDown,
    ChevronRight,
    Database,
    FileText,
    History,
    MoreVertical,
} from "lucide-react";
import { useState } from "react";
import type { Dataset } from "~/schemas/generated/dataset.schema";
import { cn } from "~/utils/classname.util";

type DatasetItemProps = {
    dataset: Dataset;
    active?: boolean;
};

function formatBytes(bytes: number) {
    if (bytes === 0) return "0 B";

    const k = 1024;
    const sizes = ["B", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return `${parseFloat((bytes / k ** i).toFixed(2))} ${sizes[i]}`;
}

export function DatasetItem({ dataset, active = false }: DatasetItemProps) {
    const { name, versions } = dataset;
    const latestVersion = versions.find((v) => v.is_latest);
    const mainArtifact = latestVersion?.artifacts.find(
        (a) => a.artifact_type === "data",
    )?.dataset_artifact;

    const type =
        latestVersion?.artifacts[0]?.artifact_type === "data" ? "CSV" : "FILE";
    const size = mainArtifact ? formatBytes(mainArtifact.size_in_bytes) : "N/A";

    const maxVersion = latestVersion?.version;

    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="flex flex-col">
            <button
                type="button"
                className={cn(
                    "group flex items-center justify-between p-2 rounded-md cursor-pointer transition-colors",
                    active
                        ? "bg-primary-500/10 text-white"
                        : "text-gray-400 hover:bg-white/5 hover:text-gray-200",
                )}
                onClick={() => setIsOpen((prev) => !prev)}
            >
                <div className="flex items-center gap-3 truncate">
                    {isOpen ? <ChevronDown size={12} /> : <ChevronRight size={12} />}

                    {type === "CSV" ? (
                        <Database size={14} className="text-blue-400" />
                    ) : (
                        <FileText size={14} className="text-orange-400" />
                    )}
                    <div className="flex flex-col truncate items-start">
                        <span className="text-xs font-medium truncate">
                            {name}
                            {maxVersion && (
                                <span className="ml-1 text-gray-500">v{maxVersion}</span>
                            )}
                        </span>
                        <span className="text-[10px] text-gray-600">
                            {size} • {type}
                        </span>
                    </div>
                </div>

                <button
                    type="button"
                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white/10 rounded transition-all cursor-pointer"
                >
                    <MoreVertical size={14} />
                </button>
            </button>

            {/* REFACTOR TO COMPONENT */}
            <AnimatePresence initial={false}>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3, ease: [0.04, 0.62, 0.23, 0.98] }}
                        className="overflow-hidden"
                    >
                        <div className="ml-7 mt-1 border-l border-border space-y-1">
                            {dataset.versions.map((version, index) => (
                                <motion.div
                                    key={version.id}
                                    initial={{ x: -8, opacity: 0 }}
                                    animate={{ x: 0, opacity: 1 }}
                                    transition={{ delay: index * 0.05 }}
                                    className="flex items-center gap-2 p-1.5 pl-3 text-[10px] text-gray-500 hover:text-gray-300 hover:bg-white/5 rounded-r-sm cursor-pointer transition-all"
                                >
                                    <History size={10} />
                                    <span>Version {version.version}</span>
                                    {version.is_latest && (
                                        <span className="ml-auto text-[8px] bg-emerald-500/10 text-emerald-500 px-1 rounded uppercase font-bold">
                                            Latest
                                        </span>
                                    )}
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
