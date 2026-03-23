import { AuthGuard } from "~/components/auth/auth-guard.component";
import { WorkspaceLayout } from "~/components/layouts/workspace.layout";
import UploadDatasetTabContent from "~/components/tabs/upload-tab/upload-tab.component";
import { WelcomeTabContent } from "~/components/tabs/welcome-tab/welcome-tab-content.component";
import { ProfileEditor } from "~/components/ui/notebook/editor.component";
import { useEditorStore } from "~/stores/editor.store";
import type { Route } from "./+types/home";

export function meta(_: Route.MetaArgs) {
	return [
		{ title: "Spectrum" },
		{
			name: "description",
			content: "The web platform for Symbolic Regression",
		},
	];
}

export default function Home() {
	const tabs = useEditorStore((s) => s.tabs);

	const activeTabId = useEditorStore((s) => s.activeTabId);
	const activeTab = activeTabId ? tabs[activeTabId] : null;

	const handleActiveTab = () => {
		if (!activeTab) {
			return <WelcomeTabContent />;
		}

		if (activeTab.type === "profile") {
			return <ProfileEditor tabId={activeTab.id} />;
		}

		return <UploadDatasetTabContent />;
	};

	return (
		<AuthGuard>
			<WorkspaceLayout>{handleActiveTab()}</WorkspaceLayout>
		</AuthGuard>
	);
}
