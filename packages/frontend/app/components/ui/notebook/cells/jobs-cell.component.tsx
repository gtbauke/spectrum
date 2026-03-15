import { useJobs } from "~/hooks/use-jobs.hook";
import type { JobsData } from "~/stores/editor.store";

type JobsCellProps = {
	id: string;
	data: JobsData;
};

export function JobsBlock({ id, data }: JobsCellProps) {
	const { data: jobs, isFetching } = useJobs({
		where: {
			profile: {
				id: data.profileId,
			},
		},
		page: 1,
	});

	if (!jobs) {
		return null;
	}

	if (isFetching) {
		return (
			<div className="p-4 text-xs text-gray-600 text-center mt-4">
				No jobs found.
			</div>
		);
	}

	return (
		<div className="space-y-2">
			<span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
				Jobs
			</span>
			<div className="rounded border border-white/5 overflow-hidden">
				{jobs?.items.map((job) => {
					if (!job.versions) {
						return null;
					}

					return (
						<div
							key={job.id}
							className="flex justify-between items-center p-3 border-b border-white/5 bg-[#111319]/50 hover:bg-white/5 transition-colors text-sm text-gray-300"
						>
							<span>{job.versions[0].name}</span>
						</div>
					);
				})}

				{jobs.items.length === 0 && (
					<div className="p-4 text-center text-xs text-gray-500">No jobs.</div>
				)}
			</div>
		</div>
	);
}
