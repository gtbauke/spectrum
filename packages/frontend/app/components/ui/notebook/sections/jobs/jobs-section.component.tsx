import { useState } from "react";
import type { Job } from "~/schemas/domain/job.schema";
import { AddButton } from "../add-button.component";
import { AddJob } from "./add-job.component";

type ProfileJobsSectionProps = {
	jobs: Job[];
};

export function ProfileJobsSection({ jobs }: ProfileJobsSectionProps) {
	const [isEditing, setIsEditing] = useState(false);

	const handleEditClick = () => {
		setIsEditing(true);
	};

	const handleSaveClick = () => {
		setIsEditing(false);
	};

	const handleCancelClick = () => {
		setIsEditing(false);
	};

	return (
		<div className="bg-background-surface border border-border rounded-lg p-4 shadow-sm space-y-2">
			<div className="flex items-center justify-between">
				<h2 className="text-lg font-semibold">Jobs</h2>

				<AddButton
					isEditing={isEditing}
					onEditClick={handleEditClick}
					onSaveClick={handleSaveClick}
					onCancelClick={handleCancelClick}
				/>
			</div>

			{isEditing && <AddJob />}

			<div className="space-y-2">
				{jobs.length === 0 && (
					<p className="text-sm text-gray-500">No jobs found.</p>
				)}
			</div>
		</div>
	);
}
