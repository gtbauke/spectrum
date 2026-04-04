import { Redo2, Save, Undo2 } from "lucide-react";
import { ta } from "zod/v4/locales";
import { useKeyboardShortcut } from "~/hooks/use-keyboard-shortcut.hook";
import { useProfileUpdateMutation } from "~/hooks/use-profile-update-mutation.hook";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";
import { ToolbarButton } from "./toolbar-button.component";

export function EditorToolbar() {
	const activeTabId = useEditorStore((state) => state.activeTabId);
	const updateTab = useEditorStore((state) => state.updateTab);
	const tabs = useEditorStore((state) => state.tabs);

	const undo = useEditorStore((state) => state.undo);
	const redo = useEditorStore((state) => state.redo);

	const { mutate, isPending } = useProfileUpdateMutation();

	const handleSave = async () => {
		if (isPending || !activeTabId) {
			return;
		}

		const tab = tabs[activeTabId];
		if (!tab || tab.type !== "profile" || !tab.data.profile) {
			return;
		}

		const currentBlocks = tab.data.blocks.filter(
			(block) => !["metadata", "datasets", "jobs"].includes(block.type),
		);

		const savedBlocks = tab.data.profile.blocks.filter(
			(block) => !["metadata", "datasets", "jobs"].includes(block.kind),
		);

		const profileId = tab.data.profile.id;
		const indexDiff = tab.data.blocks.length - currentBlocks.length;

		mutate(
			{
				profileId: profileId,
				data: {
					name: tab.data.profile.name,
					description: tab.data.profile.description,
					mode: tab.data.profile.mode,
					blocks: [], // TODO: We need to send the blocks here, but we need to transform them first to match the API schema. This will require some work to convert the editor's block format to the API's block format.
				},
			},
			{
				onSuccess: (data) => {
					updateTab(data.id, "profile", {
						isDirty: false,
						profile: data,
					});
				},
			},
		);
	};

	useKeyboardShortcut("s", handleSave);

	const tab = activeTabId ? tabs[activeTabId] : null;
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
					"flex items-center gap-2 px-3 py-1 text-[10px] rounded font-bold uppercase tracking-wider transition-all cursor-pointer",
					isDirty
						? "bg-primary text-white hover:bg-primary-700"
						: "text-gray-500 cursor-default",
				)}
				onClick={handleSave}
				disabled={isPending || !isDirty}
			>
				<Save size={12} />
				{isDirty ? "Save Changes" : "Saved"}
			</button>
		</div>
	);
}
