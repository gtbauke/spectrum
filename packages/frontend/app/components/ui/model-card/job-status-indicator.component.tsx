import type { JobStatus } from "~/schemas/job.schema";

type JobStatusIndicatorProps = {
	status: JobStatus;
};

export function JobStatusIndicator({ status }: JobStatusIndicatorProps) {
	const statusColors: Record<JobStatus, string> = {
		PENDING: "bg-yellow-500",
		QUEUED: "bg-yellow-500",
		RUNNING: "bg-blue-500",
		SUCCEEDED: "bg-green-500",
		FAILED: "bg-red-500",
		CANCELED: "bg-gray-500",
		TIMEOUT: "bg-orange-500",
		RETRYING: "bg-yellow-500",
		SKIPPED: "bg-gray-400",
		UNKNOWN: "bg-gray-300",
	};

	return (
		<span
			className={`inline-flex items-center px-2 py-1 text-xs font-medium text-white rounded ${statusColors[status]}`}
		>
			{status}
		</span>
	);
}
