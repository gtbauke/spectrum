import { useProfiles } from "~/hooks/use-profiles.hook";
import type { ProfileFilter } from "~/schemas/dtos/profile.dto";

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
				{profiles
					.filter(
						(profile) =>
							profile.name.toLowerCase().includes(filters.name || "") &&
							(filters.status ? profile.mode === filters.status : true) &&
							(filters.visibility ? profile.mode === filters.visibility : true),
					)
					.map((profile) => {
						return (
							<div key={profile.id}>
								{profile.name} - {profile.mode}
							</div>
						);
					})}
			</div>
		</div>
	);
}
