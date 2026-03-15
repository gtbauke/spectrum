import { UploadCloud } from "lucide-react";
import {
	type UploadTab,
	useProfileTabs,
} from "~/contexts/profile-tabs.context";
import { TabBase } from "./tab-base.component";

type SystemTabItemProps = {
	tab: UploadTab;
	onClick: () => void;
	onClose: () => void;
};

export function SystemTabItem({ tab, onClick, onClose }: SystemTabItemProps) {
	const { activeTabId } = useProfileTabs();
	const isActive = activeTabId === tab.id;

	return (
		<TabBase
			isActive={isActive}
			isDirty={false}
			icon={<UploadCloud size={16} className="text-gray-400" />}
			onClick={onClick}
			onClose={onClose}
		>
			<span className="truncate select-none text-gray-200">{tab.name}</span>
		</TabBase>
	);
}
