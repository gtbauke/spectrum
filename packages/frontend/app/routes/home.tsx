import { WorkspaceLayout } from "~/components/layouts/workspace.layout";
import { WelcomeTabContent } from "~/components/tabs/welcome-tab/welcome-tab-content.component";
import { useProfileTabs } from "~/contexts/profile-tabs.context";
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
    const { activeTabId } = useProfileTabs();

    return (
        <WorkspaceLayout>
            {activeTabId === null && <WelcomeTabContent />}
        </WorkspaceLayout>
    );
}
