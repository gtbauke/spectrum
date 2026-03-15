import { Folder } from "lucide-react";
import type React from "react";
import { useEffect, useRef, useState } from "react";
import { useEditorStore } from "~/stores/editor.store";
import type { ProfileTabData } from "~/utils/types/editor.types";
import { TabBase } from "./tab-base.component";

type ProfileTabItemProps = {
	tab: ProfileTabData;
	onClick: () => void;
	onClose: () => void;
};

export function ProfileTabItem({ tab, onClick, onClose }: ProfileTabItemProps) {
	const activeTabId = useEditorStore((state) => state.activeTabId);
	const updateTab = useEditorStore((state) => state.updateTab);

	const [isEditing, setIsEditing] = useState(false);
	const [tempName, setTempName] = useState(tab.name);
	const inputRef = useRef<HTMLInputElement>(null);

	const isActive = activeTabId === tab.tabId;

	useEffect(() => {
		if (isEditing) {
			inputRef.current?.focus();
			inputRef.current?.select();
		}
	}, [isEditing]);

	const handleEditSave = () => {
		setIsEditing(false);

		if (tempName.trim() && tempName !== tab.name) {
			updateTab(tab.tabId, "profile", { name: tempName.trim() });
			return;
		}

		setTempName(tab.name);
	};

	const handleKeyDown = (e: React.KeyboardEvent) => {
		if (e.key === "Enter") {
			handleEditSave();
		}

		if (e.key === "Escape") {
			setIsEditing(false);
			setTempName(tab.name);
		}
	};

	return (
		<TabBase
			isActive={isActive}
			isDirty={tab.isDirty}
			icon={<Folder size={16} />}
			onClick={onClick}
			onClose={onClose}
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
					className="truncate select-none cursor-pointer w-full"
					onDoubleClick={(e) => {
						e.stopPropagation();
						setIsEditing(true);
					}}
				>
					{tab.name}
				</button>
			)}
		</TabBase>
	);
}
