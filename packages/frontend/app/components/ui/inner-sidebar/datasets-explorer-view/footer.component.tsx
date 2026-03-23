import { Plus } from "lucide-react";
import { Button } from "~/components/ui/buttons/button.component";
import { useEditorStore } from "~/stores/editor.store";
import type { UploadTabData } from "~/utils/types/editor.types";

export function Footer() {
	const openTab = useEditorStore((state) => state.openTab);

	const onAddTabClick = () => {
		const tabId = crypto.randomUUID();
		openTab({
			type: "upload",
			id: tabId,
			data: {
				tabId,
				name: "Upload Dataset",
				file: null,
			} as UploadTabData,
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
