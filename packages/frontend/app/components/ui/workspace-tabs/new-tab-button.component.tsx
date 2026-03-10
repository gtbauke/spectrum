import { Plus } from "lucide-react";
import { useProfileTabs } from "~/contexts/profile-tabs.context";

export function NewTabButton() {
    const { openTab } = useProfileTabs();

    return (
        <button
            type="button"
            className="px-3 h-full text-gray-400 hover:text-white hover:bg-white/5 transition cursor-pointer"
            onClick={() => openTab({ id: crypto.randomUUID(), name: "New Tab" })}
        >
            <Plus size={20} />
        </button>
    )
}
