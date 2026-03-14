import { Redo2, Save, Undo2 } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";
import { ToolbarButton } from "./toolbar-button.component";

export function EditorToolbar() {
    const { undo, redo, past, future, isDirty } = useEditorStore();

    return (
        <div className="flex items-center gap-1 bg-[#1e2028]/80 backdrop-blur-md border border-white/10 rounded-xl p-1 shadow-2xl">
            <ToolbarButton
                onClick={undo}
                disabled={past.length === 0}
                icon={<Undo2 size={12} />}
                label="Undo"
                shortcut="Ctrl+Z"
            />
            <ToolbarButton
                onClick={redo}
                disabled={future.length === 0}
                icon={<Redo2 size={12} />}
                label="Redo"
                shortcut="Ctrl+Y"
            />
            <div className="w-px h-4 bg-white/10 mx-1" />
            <button
                type="button"
                className={cn(
                    "flex items-center gap-2 px-3 py-1 text-[10px] font-bold uppercase tracking-wider rounded transition-all cursor-pointer",
                    isDirty
                        ? "bg-primary-500 rounded-lg text-white shadow-lg shadow-primary-500/20"
                        : "text-gray-500 cursor-default",
                )}
            >
                <Save size={12} />
                {isDirty ? "Save Changes" : "Saved"}
            </button>
        </div>
    );
}
