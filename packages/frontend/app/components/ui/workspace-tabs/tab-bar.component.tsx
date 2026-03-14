import { useProfileTabs } from "~/contexts/profile-tabs.context";
import { NewTabButton } from "./new-tab-button.component";
import { Tab } from "./tab.component";

export function TabBar() {
    const { tabs } = useProfileTabs();

    return (
        <div className="flex items-center bg-background-surface border-b border-border h-10 overflow-x-auto no-scrollbar">
            {tabs.map((tab) => (
                <Tab key={tab.id} id={tab.id} profileName={tab.name} isDirty={tab.isDirty} />
            ))}

            <NewTabButton />
        </div>
    )
}
