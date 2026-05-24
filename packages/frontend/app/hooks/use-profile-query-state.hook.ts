import { useEffect } from "react";
import { useSearchParams } from "react-router";
import { useEditorStore } from "~/stores/editor.store";

export function useProfileQueryState() {
	const openProfileTab = useEditorStore((s) => s.openProfileTab);

	const [searchParams, setSearchParams] = useSearchParams();
	const activeTab = searchParams.get("tab") || "";

	useEffect(() => {
		if (activeTab) {
			openProfileTab(activeTab);
		}
	}, [activeTab, openProfileTab]);

	const openTab = (profileId: string) => {
		setSearchParams((prev) => {
			prev.set("tab", profileId);
			return prev;
		});

		openProfileTab(profileId);
	};

	const closeTab = () => {
		setSearchParams((prev) => {
			prev.delete("tab");
			return prev;
		});
	};

	return { openTab, activeTab, closeTab };
}
