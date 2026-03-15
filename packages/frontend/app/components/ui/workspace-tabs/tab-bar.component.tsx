import { type Tab, useProfileTabs } from "~/contexts/profile-tabs.context";
import { useEditorStore } from "~/stores/editor.store";
import { NewTabButton } from "./new-tab-button.component";
import { ProfileTabItem } from "./tabs/profile-tab.component";
import { SystemTabItem } from "./tabs/system-tab.component";

export function TabBar() {
	const { tabs, setActiveTab, closeTab } = useProfileTabs();
	const setActiveProfileId = useEditorStore(
		(state) => state.setActiveProfileId,
	);

	const handleTabClick = (tab: Tab) => {
		setActiveTab(tab.id);

		if (tab.type === "profile") {
			setActiveProfileId(tab.profileId);
			return;
		}

		setActiveProfileId(null);
	};

	const handleTabClose = (tab: Tab) => {
		const nextOpenTab = closeTab(tab.id);
		setActiveProfileId(nextOpenTab);
	};

	return (
		<div className="flex items-center bg-background-surface border-b border-border h-10 overflow-x-auto no-scrollbar">
			{tabs.map((tab) => {
				if (tab.type !== "profile") {
					return (
						<SystemTabItem
							key={tab.id}
							tab={tab}
							onClick={() => handleTabClick(tab)}
							onClose={() => handleTabClose(tab)}
						/>
					);
				}

				return (
					<ProfileTabItem
						key={tab.id}
						tab={tab}
						onClick={() => handleTabClick(tab)}
						onClose={() => handleTabClose(tab)}
					/>
				);
			})}

			<NewTabButton />
		</div>
	);
}
