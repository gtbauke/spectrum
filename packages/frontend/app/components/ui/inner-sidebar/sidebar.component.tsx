import {
	type ActivityView,
	useActivity,
} from "~/contexts/activity-view.context";
import { DatasetExplorer } from "./datasets-explorer-view/sidebar.component";
import { JobsExplorer } from "./jobs-explorer-view/sidebar.component";
import { ProfilesExplorer } from "./profiles-explorer-view/sidebar.component";

export function InnerSidebar() {
	const { activeView } = useActivity();

	const renderActiveView = (view: ActivityView) => {
		switch (view) {
			case "datasets":
				return <DatasetExplorer />;
			case "profiles":
				return <ProfilesExplorer />;
			case "jobs":
				return <JobsExplorer />;
			default:
				return <div>ERROR</div>;
		}
	};

	return (
		<aside className="w-64 border-r border-border bg-[#111319] flex flex-col">
			{renderActiveView(activeView)}
		</aside>
	);
}
