import {
    MdOutlineAccountCircle,
    MdOutlineSearch,
    MdOutlineSettings,
    MdOutlineTimer,
    MdOutlineWorkspaces,
} from "react-icons/md";
import { ActivityIcon } from "./icon.component";

export function ActivitySidebar() {
    return (
        <aside className="w-16 flex flex-col items-center py-4 bg-background-bg-conic-0 border-r border-border shrink-0">
            <nav className="flex flex-col space-y-4">
                <ActivityIcon
                    Icon={MdOutlineWorkspaces}
                    label="Profiles"
                    activityView="profiles"
                />

                <ActivityIcon
                    Icon={MdOutlineSearch}
                    label="Global Datasets"
                    activityView="datasets"
                />

                <ActivityIcon
                    Icon={MdOutlineTimer}
                    label="Job Monitor"
                    activityView="jobs"
                />
            </nav>

            <div className="mt-auto flex flex-col space-y-4">
                <ActivityIcon
                    Icon={MdOutlineAccountCircle}
                    label="My account"
                    activityView="account"
                />

                <ActivityIcon
                    Icon={MdOutlineSettings}
                    label="Settings"
                    activityView="settings"
                />
            </div>
        </aside>
    );
}
