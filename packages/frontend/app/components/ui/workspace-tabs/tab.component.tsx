import { MdClose, MdOutlineFolderOpen } from "react-icons/md";
import { useProfileTabs } from "~/contexts/profile-tabs.context";
import { cn } from "~/utils/classname.util";

type TabProps = {
    id: string;
    profileName: string;
};

export function Tab({ id, profileName }: TabProps) {
    const { activeTabId, closeTab } = useProfileTabs();
    const isActive = activeTabId === id;

    return (
        <div className={cn(
            "flex items-center px-4 h-full bg-background text-sm cursor-pointer group gap-2",
            isActive ? "border-t-2 border-primary-500" : ""
        )}>
            <div className="flex items-center gap-2">
                <span className="text-primary-400">
                    <MdOutlineFolderOpen size={16} />
                </span>
                <span>{profileName}</span>
            </div>

            <button
                type="button"
                className="opacity-0 group-hover:opacity-100 hover:text-red-400 cursor-pointer"
                onClick={() => closeTab(id)}
            >
                <MdClose size={16} />
            </button>
        </div>
    )
}
