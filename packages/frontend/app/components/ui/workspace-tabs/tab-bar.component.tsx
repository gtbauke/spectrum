import { useEditorStore } from "~/stores/editor.store";
import type { EditorTab } from "~/utils/types/editor.types";
import { NewTabButton } from "./new-tab-button.component";
import { DatasetTabItem } from "./tabs/dataset-tab.component";
import { ProfileTabItem } from "./tabs/profile-tab.component";
import { SystemTabItem } from "./tabs/system-tab.component";

export function TabBar() {
	const tabs = useEditorStore((state) => state.tabs);
	const tabIds = useEditorStore((state) => state.tabIds);
	const setActiveTab = useEditorStore((state) => state.setActiveTab);
	const closeTab = useEditorStore((state) => state.closeTab);

	const handleTabClick = (tab: EditorTab) => {
		setActiveTab(tab.id);

		if (tab.type === "profile" || tab.type === "dataset") {
			setActiveTab(tab.id);
			return;
		}

		setActiveTab(null);
	};

	const handleTabClose = (tab: EditorTab) => {
		closeTab(tab.id);
	};

	return (
		<div className="flex items-center bg-background-surface border-b border-border h-10 overflow-x-auto no-scrollbar">
			{tabIds.map((tabId) => {
				const tab = tabs[tabId];

				if (tab.type === "upload") {
					return (
						<SystemTabItem
							key={tab.id}
							tab={tab.data}
							onClick={() => handleTabClick(tab)}
							onClose={() => handleTabClose(tab)}
						/>
					);
				}

				if (tab.type === "dataset") {
					return (
						<DatasetTabItem
							key={tab.id}
							tab={tab.data}
							onClick={() => handleTabClick(tab)}
							onClose={() => handleTabClose(tab)}
						/>
					);
				}

				return (
					<ProfileTabItem
						key={tab.id}
						tab={tab.data}
						onClick={() => handleTabClick(tab)}
						onClose={() => handleTabClose(tab)}
					/>
				);
			})}

			<NewTabButton />
		</div>
	);
}
