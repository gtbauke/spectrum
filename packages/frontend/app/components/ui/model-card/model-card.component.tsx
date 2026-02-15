import { FaPencilAlt, FaTrash, FaUndo } from "react-icons/fa";
import { useRevalidator } from "react-router";
import { runModel } from "~/api/run-model.api";
import type { Model } from "~/schemas/model.schema";
import { JobStatusIndicator } from "./job-status-indicator.component";

type ModelCardProps = {
	model: Model;
};

export function ModelCard({ model }: ModelCardProps) {
	const revalidator = useRevalidator();

	const handleRunModel = async () => {
		try {
			await runModel(model.id);
			await revalidator.revalidate();
		} catch (error) {
			console.error("Error running model:", error);
			return;
		}
	};

	return (
		<div className="border p-4 rounded shadow space-y-4 border-gray-800 w-full">
			<header className="space-y-1">
				<div className="flex items-center justify-between">
					<div className="flex items-center gap-2">
						<h3 className="text-lg font-semibold">{model.name}</h3>
						<p className="text-xs text-gray-500">
							(Created at {model.created_at.toDateString()})
						</p>
					</div>

					<div className="flex space-x-4">
						<button
							type="button"
							className="text-red-500 hover:text-red-700 active:text-red-800 cursor-pointer"
						>
							<FaTrash size={12} />
						</button>

						<button
							type="button"
							className="text-blue-500 hover:text-blue-700 active:text-blue-800 cursor-pointer"
						>
							<FaPencilAlt size={12} />
						</button>

						<button
							type="button"
							className="text-green-500 hover:text-green-700 active:text-green-800 cursor-pointer"
							onClick={handleRunModel}
						>
							<FaUndo size={12} />
						</button>
					</div>
				</div>

				<p className="text-xs text-gray-500">{model.id}</p>
			</header>

			<div>
				{model.job ? (
					<JobStatusIndicator status={model.job.status} />
				) : (
					<span className="text-sm text-gray-500">No job associated</span>
				)}
			</div>
		</div>
	);
}
