import { useNavigate } from "react-router";
import type { JobStatus } from "~/schemas/job.schema";
import { cn } from "~/utils/classname.util";

type EnterPlaygroundButtonProps = {
	jobStatus: JobStatus;
	modelId: string;
};

export function EnterPlaygroundButton({
	jobStatus,
	modelId,
}: EnterPlaygroundButtonProps) {
	const navigate = useNavigate();
	const isDisabled = jobStatus !== "SUCCEEDED";

	const handleClick = () => {
		navigate(`/playground/${modelId}`);
	};

	return (
		<button
			type="button"
			disabled={isDisabled}
			className={cn(
				"px-4 py-2 rounded text-sm font-medium cursor-pointer",
				isDisabled
					? "bg-gray-300 text-gray-500 cursor-not-allowed"
					: "bg-blue-500 text-white hover:bg-blue-600 active:bg-blue-700",
			)}
			onClick={handleClick}
		>
			Enter Playground
		</button>
	);
}
