import { useProfileTabs } from "~/contexts/profile-tabs.context";
import { NewTabButton } from "./new-tab-button.component";
import { ProfileTabItem } from "./tabs/profile-tab.component";
import { SystemTabItem } from "./tabs/system-tab.component";

export function TabBar() {
	const { tabs } = useProfileTabs();

	return (
		<div className="flex items-center bg-background-surface border-b border-border h-10 overflow-x-auto no-scrollbar">
			{tabs.map((tab) => {
				if (tab.type !== "profile") {
					return <SystemTabItem key={tab.id} tab={tab} />;
				}

				return <ProfileTabItem key={tab.id} tab={tab} />;
			})}

			<NewTabButton />
		</div>
	);
}
