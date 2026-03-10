import {
    CircleUserRound,
    FolderSearch,
    Settings,
    Timer,
    Workflow,
} from "lucide-react";
import { ActivityButton } from "./activity-button.component";

export function ActivitySidebar() {
    return (
        <aside className="w-16 flex flex-col items-center py-4 bg-background-bg-conic-0 border-r border-border shrink-0">
            <nav className="flex flex-col space-y-4">
                <ActivityButton
                    Icon={Workflow}
                    label="Profiles"
                    activityView="profiles"
                />

                <ActivityButton
                    Icon={FolderSearch}
                    label="Global Datasets"
                    activityView="datasets"
                />

                <ActivityButton
                    Icon={Timer}
                    label="Job Monitor"
                    activityView="jobs"
                />
            </nav>

            <div className="mt-auto flex flex-col space-y-4">
                <ActivityButton
                    Icon={CircleUserRound}
                    label="My account"
                    activityView="account"
                />

                <ActivityButton
                    Icon={Settings}
                    label="Settings"
                    activityView="settings"
                />
            </div>
        </aside>
    );
}
