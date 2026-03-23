import { Redo2, Save, Undo2 } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";
import { ToolbarButton } from "./toolbar-button.component";

export function EditorToolbar() {
	const activeTabId = useEditorStore((state) => state.activeTabId);
	const tab = useEditorStore((state) =>
		activeTabId ? state.tabs[activeTabId] : null,
	);

	const undo = useEditorStore((state) => state.undo);
	const redo = useEditorStore((state) => state.redo);

	if (!tab || tab.type !== "profile") {
		return null;
	}

	const { past, future, isDirty } = tab.data;

	return (
		<div className="flex items-center gap-1 bg-background-surface border border-border p-1 transition-all duration-200">
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
			<div className="w-px h-4 bg-border mx-1" />
			<button
				type="button"
				className={cn(
					"flex items-center gap-2 px-3 py-1 text-[10px] font-bold uppercase tracking-wider transition-all",
					isDirty
						? "bg-primary text-white hover:bg-primary-hover"
						: "text-gray-500 cursor-default",
				)}
			>
				<Save size={12} />
				{isDirty ? "Save Changes" : "Saved"}
			</button>
		</div>
	);
}
