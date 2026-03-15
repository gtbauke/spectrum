import { UploadCloud } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";
import { capitalize } from "~/utils/capitalize.util";
import type { UploadTabData } from "~/utils/types/editor.types";
import { TabBase } from "./tab-base.component";

type SystemTabItemProps = {
	tab: UploadTabData;
	onClick: () => void;
	onClose: () => void;
};

export function SystemTabItem({ tab, onClick, onClose }: SystemTabItemProps) {
	const activeTabId = useEditorStore((state) => state.activeTabId);
	const isActive = activeTabId === tab.tabId;

	return (
		<TabBase
			isActive={isActive}
			isDirty={false}
			icon={<UploadCloud size={16} className="text-gray-400" />}
			onClick={onClick}
			onClose={onClose}
		>
			<span className="truncate select-none text-gray-200">
				{capitalize(tab.name)}
			</span>
		</TabBase>
	);
}
