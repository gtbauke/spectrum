import { useState } from "react";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import type { Job } from "~/schemas/domain/job.schema";
import { AddButton } from "../add-button.component";
import { AddJob } from "./add-job.component";
import { JobItem } from "./job-item.component";

type ProfileJobsSectionProps = {
	profileId: string;
	jobs: Job[];
	datasets: Dataset[];
};

export function ProfileJobsSection({
	profileId,
	jobs,
	datasets,
}: ProfileJobsSectionProps) {
	const [isEditing, setIsEditing] = useState(false);

	return (
		<div className="bg-background-surface border border-border rounded-lg p-4 shadow-sm space-y-2">
			<div className="flex items-center justify-between">
				<h2 className="text-lg font-semibold">Jobs</h2>

				<AddButton
					isEditing={isEditing}
					onEditClick={() => setIsEditing(true)}
					onSaveClick={() => setIsEditing(false)}
					onCancelClick={() => setIsEditing(false)}
				/>
			</div>

			{isEditing && (
				<AddJob
					profileId={profileId}
					datasets={datasets}
					onSuccess={() => setIsEditing(false)}
					onCancel={() => setIsEditing(false)}
				/>
			)}

			<div className="space-y-3">
				{jobs.length === 0 && (
					<p className="text-sm text-gray-500">No jobs found.</p>
				)}

				{jobs.map((job) => (
					<JobItem key={job.id} job={job} datasets={datasets} />
				))}
			</div>
		</div>
	);
}
