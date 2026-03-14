import { UploadCloud } from "lucide-react";
import {
	type UploadTab,
	useProfileTabs,
} from "~/contexts/profile-tabs.context";
import { TabBase } from "./tab-base.component";

type SystemTabItemProps = {
	tab: UploadTab;
};

export function SystemTabItem({ tab }: SystemTabItemProps) {
	const { activeTabId, closeTab, setActiveTab } = useProfileTabs();
	const isActive = activeTabId === tab.id;

	return (
		<TabBase
			isActive={isActive}
			isDirty={false}
			icon={<UploadCloud size={16} className="text-gray-400" />}
			onClick={() => setActiveTab(tab.id)}
			onClose={() => closeTab(tab.id)}
		>
			<span className="truncate select-none text-gray-200">{tab.name}</span>
		</TabBase>
	);
}
