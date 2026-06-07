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

	const [searchParams, setSearchParams] = useSearchParams();
	const queryTab = searchParams.get("tab") || "";

	const openTab = useCallback(
		(profileId: string) => {
			setSearchParams((prev) => {
				prev.set("tab", profileId);
				return prev;
			});

			openProfileTab(profileId);
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

	return { openTab, activeTab: queryTab, closeTab };
}
