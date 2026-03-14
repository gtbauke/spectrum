import { AuthGuard } from "~/components/auth/auth-guard.component";
import { WorkspaceLayout } from "~/components/layouts/workspace.layout";
import { WelcomeTabContent } from "~/components/tabs/welcome-tab/welcome-tab-content.component";
import { ProfileEditor } from "~/components/ui/notebook/editor.component";
import { useProfileTabs } from "~/contexts/profile-tabs.context";
import type { Route } from "./+types/home";
import UploadDatasetTabContent from "~/components/tabs/upload-tab/upload-tab.component";

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
    const { activeTabId, tabs } = useProfileTabs();
    const activeTab = tabs.find((tab) => tab.id === activeTabId);

    const handleActiveTab = () => {
        if (!activeTab) {
            return <WelcomeTabContent/>
        }

        if (activeTab.type === "profile") {
            return <ProfileEditor version={activeTab.profileVersion} />
        }

        return <UploadDatasetTabContent/>
    };

    return (
        <AuthGuard>
            <WorkspaceLayout>
                {handleActiveTab()}
            </WorkspaceLayout>
        </AuthGuard>
    );
}
