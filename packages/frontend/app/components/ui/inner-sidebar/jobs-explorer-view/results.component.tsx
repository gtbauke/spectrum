import { useFullProfiles } from "~/hooks/use-profiles.hook";
import type { ProfileFilter } from "~/schemas/dtos/profile.dto";

type ResultsProps = {
	filters: ProfileFilter;
};

export function Results({ filters }: ResultsProps) {
	const { data, isLoading } = useFullProfiles(filters);
	const profiles = data?.pages.flatMap((page) => page.items) || [];

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
			<div className="flex-1 overflow-y-auto p-2 space-y-4 custom-scrollbar">
				{profiles
					.filter(
						(profile) =>
							profile.name.toLowerCase().includes(filters.name || "") &&
							(filters.status ? profile.mode === filters.status : true) &&
							(filters.visibility ? profile.mode === filters.visibility : true),
					)
					.map((profile) => {
						const runs =
							profile.jobs
								?.flatMap((job) => job.runs)
								.sort((a, b) => {
									const dateA = a.startedAt
										? new Date(a.startedAt).getTime()
										: 0;
									const dateB = b.startedAt
										? new Date(b.startedAt).getTime()
										: 0;

									return dateB - dateA;
								}) || [];

						return (
							<div
								key={profile.id}
								className="rounded-md hover:bg-primary/20 space-y-1 pb-2"
							>
								<div className="p-2 flex flex-row gap-2 items-center">
									<div className="text-sm font-medium">{profile.name}</div>
									<div className="text-xs text-gray-500">
										{profile.mode.toUpperCase()}
									</div>
								</div>

								<div>
									{runs.length > 0 ? (
										<ul className="space-y-1">
											{runs.map((run) => (
												<li
													key={run.id}
													className="text-xs flex items-center gap-2 px-2 py-1"
												>
													<div
														className={`px-2 py-1 rounded-full ${
															run.status === "finished"
																? "bg-green-500"
																: run.status === "failed"
																	? "bg-red-500"
																	: "bg-yellow-500"
														}`}
													>
														{run.status.toUpperCase()}
													</div>

													<div>
														{run.startedAt
															? new Date(run.startedAt).toLocaleString()
															: "N/A"}
													</div>
												</li>
											))}
										</ul>
									) : (
										<div className="text-xs text-gray-500 flex items-center justify-center">
											No runs found for this profile.
										</div>
									)}
								</div>
							</div>
						);
					})}
			</div>
		</div>
	);
}
