import {
    CircleUserRound,
    FolderSearch,
    Settings,
    Timer,
    Workflow,
} from "lucide-react";
import { ActivityIcon } from "./icon.component";

export function ActivitySidebar() {
    return (
        <aside className="w-16 flex flex-col items-center py-4 bg-background-bg-conic-0 border-r border-border shrink-0">
            <nav className="flex flex-col space-y-4">
                <ActivityIcon
                    Icon={Workflow}
                    label="Profiles"
                    activityView="profiles"
                />

                <ActivityIcon
                    Icon={FolderSearch}
                    label="Global Datasets"
                    activityView="datasets"
                />

                <ActivityIcon
                    Icon={Timer}
                    label="Job Monitor"
                    activityView="jobs"
                />
            </nav>

            <div className="mt-auto flex flex-col space-y-4">
                <ActivityIcon
                    Icon={CircleUserRound}
                    label="My account"
                    activityView="account"
                />

                <ActivityIcon
                    Icon={Settings}
                    label="Settings"
                    activityView="settings"
                />
            </div>
        </aside>
    );
}
