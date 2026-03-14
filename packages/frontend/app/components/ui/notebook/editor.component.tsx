import { AnimatePresence, motion } from "framer-motion";
import { useEffect } from "react";
import { NotebookCell } from "~/components/ui/notebook/cell.component";
import { useKeyboardShortcut } from "~/hooks/use-keyboard-shortcut.hook";
import type { ProfileVersion } from "~/schemas/generated/profile-version.schema";
import { type EditorBlock, useEditorStore } from "~/stores/editor.store";
import { DatasetsBlock } from "./cells/datasets-cell.component";
import { InferenceBlock } from "./cells/inference-cell.component";
import { MarkdownBlock } from "./cells/markdown-cell.component";
import { MetadataBlock } from "./cells/metadata-cell.component";
import { EditorToolbar } from "./editor-toolbar.component";
import { InsertDivider } from "./insert-divider.component";

type ProfileEditorProps = {
    version: ProfileVersion;
};

export function ProfileEditor({ version }: ProfileEditorProps) {
    const initEditor = useEditorStore((state) => state.initEditor);
    const blocks = useEditorStore((state) => state.blocks);
    const activeBlockId = useEditorStore((state) => state.activeBlockId);
    const setActiveBlock = useEditorStore((state) => state.setActiveBlock);

    const undo = useEditorStore((state) => state.undo);
    const redo = useEditorStore((state) => state.redo);

    useKeyboardShortcut("z", undo);
    useKeyboardShortcut("y", redo);

    useEffect(() => {
        const dynamic_blocks: EditorBlock[] = [];

        for (const block of version.blocks) {
            dynamic_blocks.push({
                id: block.id,
                type: block.type,
                // biome-ignore lint/suspicious/noExplicitAny: Value is dynamic
                data: block.data as any,
            });
        }

        initEditor(version.profile_id, version.id, [
            {
                id: "metadata",
                type: "metadata",
                data: {
                    name: version.name,
                    description: version.description,
                    visibility: version.visibility,
                },
            },
            {
                id: "datasets",
                type: "datasets",
                data: {
                    datasets: version.datasets,
                },
            },
            ...dynamic_blocks,
        ]);
    }, [version, initEditor]);

    if (!blocks.length) {
        return null;
    }

    return (
        <div className="flex-1 h-full overflow-y-auto custom-scrollbar bg-[#111319] py-8 px-4">
            <div className="sticky top-0 z-40 w-full flex justify-center py-4 pointer-events-none">
                <div className="pointer-events-auto">
                    <EditorToolbar />
                </div>
            </div>

            <div className="max-w-4xl mx-auto mb-8 pl-12">
                <h1 className="text-2xl font-bold text-gray-200">{version.name}</h1>
                <p className="text-xs text-gray-500 mt-1">
                    Version {version.version} • {version.status}
                </p>
            </div>

            <AnimatePresence initial={false} mode="popLayout">
                {blocks.map((block, index) => (
                    <motion.div
                        layout
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{
                            opacity: 0,
                            height: 0,
                            scale: 0.95,
                            transition: { opacity: { duration: 0.1 } },
                        }}
                        key={block.id}
                    >
                        <InsertDivider index={index} />

                        <NotebookCell
                            id={block.id}
                            type={block.type}
                            isActive={activeBlockId === block.id}
                            onClick={() => setActiveBlock(block.id)}
                            isDeletable={!["metadata", "dataset"].includes(block.type)}
                            moveable={!["metadata", "dataset"].includes(block.type)}
                        >
                            {block.type === "metadata" && (
                                <MetadataBlock id={block.id} data={block.data} />
                            )}
                            {block.type === "datasets" && (
                                <DatasetsBlock datasets={block.data.datasets} />
                            )}
                            {block.type === "inference" && (
                                <InferenceBlock id={block.id} data={block.data} />
                            )}
                            {block.type === "markdown" && (
                                <MarkdownBlock
                                    id={block.id}
                                    data={block.data}
                                    isActive={activeBlockId === block.id}
                                />
                            )}
                        </NotebookCell>

                        {index === blocks.length - 1 && <InsertDivider index={index + 1} />}
                    </motion.div>
                ))}
            </AnimatePresence>

            <div className="h-64" />
        </div>
    );
}
