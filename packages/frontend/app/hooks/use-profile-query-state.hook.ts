import { useCallback, useEffect } from "react";
import { useSearchParams } from "react-router";
import { useEditorStore } from "~/stores/editor.store";

type UseProfileQueryStateOptions = {
	onClose?: () => void;
};

export function useProfileQueryState(
	options: UseProfileQueryStateOptions = {},
) {
	const openProfileTab = useEditorStore((s) => s.openProfileTab);
	const closeProfileTab = useEditorStore((s) => s.closeTab);
	const activeTabId = useEditorStore((s) => s.activeTabId);
	const setActiveTab = useEditorStore((s) => s.setActiveTab);

	const [searchParams, setSearchParams] = useSearchParams();
	const queryTab = searchParams.get("tab") || "";

	const openTab = useCallback(
		(profileId: string, tabName: string = "Untitled Profile") => {
			setSearchParams((prev) => {
				prev.set("tab", profileId);
				return prev;
			});

			openProfileTab(profileId, tabName);
		},
		[openProfileTab, setSearchParams],
	);

	useEffect(() => {
		if (!queryTab && activeTabId) {
			openTab(activeTabId);
		}
	}, [queryTab, activeTabId, openTab]);

	const closeTab = (tabId: string) => {
		setSearchParams((prev) => {
			prev.delete("tab");
			return prev;
		});

		options.onClose?.();
		closeProfileTab(tabId);
	};

	const setActiveQueryTab = (newTabId: string) => {
		setActiveTab(newTabId);
		setSearchParams((prev) => {
			prev.set("tab", newTabId);
			return prev;
		});
	};

	return { openTab, activeTab: queryTab, closeTab, setActiveQueryTab };
}
