import { useProfiles } from "~/hooks/use-profiles.hook";
import type { ProfileFilter } from "~/schemas/dtos/profile.dto";
import { ProfileItem } from "./profile-item.component";

type ResultsProps = {
	filters: ProfileFilter;
};

export function Results({ filters }: ResultsProps) {
	const { data: profiles, isLoading } = useProfiles();

	if (isLoading) {
		return (
			<div className="p-4 text-xs text-gray-500 animate-pulse">
				Loading profiles...
			</div>
		);
	}

	if (!profiles || profiles.length === 0) {
		return <div className="p-4 text-xs text-gray-500">No profiles found.</div>;
	}

	return (
		<div className="flex-1 flex flex-col overflow-hidden">
			<div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
				{profiles.map((profile) => {
					return <ProfileItem key={profile.id} profile={profile} />;
				})}
			</div>
		</div>
	);
}
