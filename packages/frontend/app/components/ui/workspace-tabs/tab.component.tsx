import { Folder, X } from "lucide-react";
import type React from "react";
import { useEffect, useRef, useState } from "react";
import { useProfileTabs } from "~/contexts/profile-tabs.context";
import { cn } from "~/utils/classname.util";

type TabProps = {
    id: string;
    profileName: string;
    isDirty?: boolean;
};

export function Tab({ id, profileName, isDirty = false }: TabProps) {
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
            updateTab(id, { name: tempName.trim(), isDirty: true });
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

    const handleTabSwitch = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        e.stopPropagation();
        setActiveTab(id);
    };

    const onKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") {
            setActiveTab(id);
        }
    };

    return (
        // biome-ignore lint/a11y/useSemanticElements: Cannot have nested buttons
        <div role="button" tabIndex={0} className="h-full cursor-pointer" onClick={handleTabSwitch} onKeyDown={onKeyDown}>
            <div
                className={cn(
                    "flex items-center px-4 h-full text-sm cursor-pointer group gap-2",
                    isActive
                        ? "border-t-2 border-primary-500 bg-background"
                        : "bg-background-surface",
                )}
            >
                <div className="flex items-center gap-2 cursor-pointer">
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
                            className="truncate select-none cursor-pointer"
                            onDoubleClick={handleDoubleClick}
                        >
                            {profileName}
                        </button>
                    )}
                </div>

                <div className="relative flex items-center justify-center w-6 h-6 ml-2 cursor-pointer">
                    <div
                        className={cn(
                            "absolute w-2 h-2 rounded-full bg-white transition-opacity duration-200",
                            isDirty ? "opacity-100 group-hover:opacity-0" : "opacity-0"
                        )}
                    />

                    <button
                        type="button"
                        className={cn(
                            "absolute p-1 text-gray-400 hover:text-red-400 cursor-pointer rounded-md transition-opacity duration-200",
                            "opacity-0 group-hover:opacity-100 focus-visible:opacity-100 outline-none focus-visible:ring-1 focus-visible:ring-primary-500",
                            isActive && !isDirty ? "opacity-100" : "",
                            isActive ? "hover:bg-background-surface" : "hover:bg-background",
                        )}
                        onClick={handleTabClose}
                        title="Close Tab"
                    >
                        <X size={14} />
                    </button>
                </div>
            </div>
        </div>
    );
}
