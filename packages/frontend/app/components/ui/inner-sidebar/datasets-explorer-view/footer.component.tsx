import { Plus } from "lucide-react";
import { Button } from "~/components/ui/buttons/button.component";
import { useEditorStore } from "~/stores/editor.store";

export function Footer() {
	const openTab = useEditorStore((state) => state.openTab);

	const onAddTabClick = () => {
		openTab({
			type: "upload",
			id: crypto.randomUUID(),
			data: {
				file: null,
			},
		});
	};

	return (
		<div className="p-4 border-t border-border shrink-0">
			<Button type="button" onClick={onAddTabClick}>
				<div className="flex items-center gap-2 w-full justify-center">
					<Plus size={14} />{" "}
					<span className="text-xs font-medium">Import Dataset</span>
				</div>
			</Button>
		</div>
	);
}
