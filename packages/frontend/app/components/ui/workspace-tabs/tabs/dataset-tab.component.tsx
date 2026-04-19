import { Table } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";
import type { DatasetTabData } from "~/utils/types/editor.types";
import { TabBase } from "./tab-base.component";

type DatasetTabItemProps = {
	tab: DatasetTabData;
	onClick: () => void;
	onClose: () => void;
};

export function DatasetTabItem({ tab, onClick, onClose }: DatasetTabItemProps) {
	const activeTabId = useEditorStore((state) => state.activeTabId);
	const isActive = activeTabId === tab.tabId;

	return (
		<TabBase
			isActive={isActive}
			isDirty={false}
			icon={<Table size={16} className="text-gray-400" />}
			onClick={onClick}
			onClose={onClose}
		>
			<span className="truncate select-none text-gray-200">Dataset</span>
		</TabBase>
	);
}
