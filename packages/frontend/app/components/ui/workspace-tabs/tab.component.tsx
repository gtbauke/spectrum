import { Folder, X } from "lucide-react";
import type React from "react";
import { useEffect, useRef, useState } from "react";
import { useProfileTabs } from "~/contexts/profile-tabs.context";
import { cn } from "~/utils/classname.util";

type TabProps = {
    id: string;
    profileName: string;
};

export function Tab({ id, profileName }: TabProps) {
    const { activeTabId, closeTab, setActiveTab, updateTab } = useProfileTabs();

    const [isEditing, setIsEditing] = useState(false);
    const [tempName, setTempName] = useState(profileName);

    const inputRef = useRef<HTMLInputElement>(null);
    const isActive = activeTabId === id;

    useEffect(() => {
        if (isEditing) {
            inputRef.current?.focus();
            inputRef.current?.select();
        }
    }, [isEditing]);

    const handleEditSave = () => {
        setIsEditing(false);

        if (tempName.trim() && tempName !== profileName) {
            updateTab(id, { name: tempName.trim() });
            return;
        }

        setTempName(profileName);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") {
            handleEditSave();
        }

        if (e.key === "Escape") {
            setIsEditing(false);
            setTempName(profileName);
        }
    };

    const handleTabClose = (e: React.MouseEvent) => {
        e.stopPropagation();
        closeTab(id);
    };

    const handleDoubleClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsEditing(true);
    };

    const handleTabSwitch = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.stopPropagation();
        setActiveTab(id);
    };

    return (
        <button type="button" className="h-full" onClick={handleTabSwitch}>
            <div
                className={cn(
                    "flex items-center px-4 h-full text-sm cursor-pointer group gap-2",
                    isActive
                        ? "border-t-2 border-primary-500 bg-background"
                        : "bg-background-surface",
                )}
            >
                <div className="flex items-center gap-2">
                    <span className="text-primary-400">
                        <Folder size={16} />
                    </span>

                    {isEditing ? (
                        <input
                            ref={inputRef}
                            type="text"
                            value={tempName}
                            onChange={(e) => setTempName(e.target.value)}
                            onBlur={handleEditSave}
                            onKeyDown={handleKeyDown}
                            className="bg-background-surface border border-primary-500 rounded px-1 outline-none w-32 text-white"
                        />
                    ) : (
                        <button
                            type="button"
                            className="truncate select-none"
                            onDoubleClick={handleDoubleClick}
                        >
                            {profileName}
                        </button>
                    )}
                </div>

                <button
                    type="button"
                    className={cn(
                        "opacity-0 p-1 group-hover:opacity-100 hover:text-red-400 cursor-pointer rounded-md",
                        isActive ? "hover:bg-background-surface" : "hover:bg-background",
                    )}
                    onClick={handleTabClose}
                >
                    <X size={16} />
                </button>
            </div>
        </button>
    );
}
