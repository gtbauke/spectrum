import { Folder } from "lucide-react";
import type React from "react";
import { useEffect, useRef, useState } from "react";
import { useProfileQueryState } from "~/hooks/use-profile-query-state.hook";
import { useEditorStore } from "~/stores/editor.store";
import type { ProfileTabData } from "~/utils/types/editor.types";
import { TabBase } from "./tab-base.component";

type ProfileTabItemProps = {
	tab: ProfileTabData;
	onClick: () => void;
};

export function ProfileTabItem({ tab, onClick }: ProfileTabItemProps) {
	const { closeTab } = useProfileQueryState();

	const activeTabId = useEditorStore((state) => state.activeTabId);
	const updateTab = useEditorStore((state) => state.updateTab);

	const [isEditing, setIsEditing] = useState(false);
	const [tempName, setTempName] = useState(tab.profile?.name || "Untitled");
	const inputRef = useRef<HTMLInputElement>(null);

	const isActive = activeTabId === tab.tabId;

	const profileName = tab.profile?.name || "Untitled";

	useEffect(() => {
		if (isEditing) {
			inputRef.current?.focus();
			inputRef.current?.select();
		}
	}, [isEditing]);

	const handleEditSave = () => {
		setIsEditing(false);

		if (tempName.trim() && tempName !== profileName) {
			if (tab.profile) {
				updateTab(tab.tabId, "profile", {
					profile: { ...tab.profile, name: tempName.trim() },
				});
			}
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

	const handleClose = () => {
		closeTab(tab.tabId);
	};

	return (
		<TabBase
			isActive={isActive}
			isDirty={tab.isDirty}
			icon={<Folder size={16} />}
			onClick={onClick}
			onClose={handleClose}
		>
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
					className="truncate select-none cursor-pointer w-full text-xs font-medium"
					onDoubleClick={(e) => {
						e.stopPropagation();
						setIsEditing(true);
					}}
				>
					{profileName}
				</button>
			)}
		</TabBase>
	);
}
