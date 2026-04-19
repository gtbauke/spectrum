import { Clock } from "lucide-react";
import { ProfileItem } from "~/components/ui/inner-sidebar/profiles-explorer-view/profile-item.component";
import { useRecentProfiles } from "~/hooks/use-recent-profiles.hook";

export function ProfileHistory() {
	const { data: recentProfiles, isFetching } = useRecentProfiles();

	if (isFetching) {
		return <div>Loading...</div>;
	}

	return (
		<div className="mt-8 w-full max-w-2xl bg-background-surface/50 border border-border rounded-xl p-6 backdrop-blur-sm">
			<div className="flex items-center gap-2 mb-4 text-xs font-bold uppercase tracking-widest text-gray-500">
				<Clock size={14} /> Recent Profiles
			</div>
			<div className="space-y-2">
				{recentProfiles?.map((item) => (
					<ProfileItem
						key={item.id}
						profile={item}
						lastUpdated={item.updatedAt}
					/>
				))}
			</div>
		</div>
	);
}
