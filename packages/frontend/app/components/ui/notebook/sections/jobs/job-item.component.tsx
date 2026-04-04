import {
	CheckCircle,
	ChevronDown,
	ChevronUp,
	Clock,
	Play,
	PlayIcon,
	Trash,
	XCircle,
} from "lucide-react";
import { useState } from "react";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import { useJobDeleteMutation } from "~/hooks/use-job-delete-mutation.hook";
import { useRunJobMutation } from "~/hooks/use-run-job-mutation.hook";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import type { Job, Run } from "~/schemas/domain/job.schema";

type JobItemProps = {
	job: Job;
	datasets: Dataset[];
};

function StatusBadge({ status }: { status: Run["status"] | "no_runs" }) {
	switch (status) {
		case "finished":
			return (
				<span className="flex items-center gap-1 bg-green-500/10 text-green-500 text-xs px-2 py-1 rounded-md font-medium border border-green-500/20">
					<CheckCircle size={12} />
					Finished
				</span>
			);
		case "failed":
			return (
				<span className="flex items-center gap-1 bg-red-500/10 text-red-500 text-xs px-2 py-1 rounded-md font-medium border border-red-500/20">
					<XCircle size={12} />
					Failed
				</span>
			);
		case "running":
			return (
				<span className="flex items-center gap-1 bg-blue-500/10 text-blue-500 text-xs px-2 py-1 rounded-md font-medium border border-blue-500/20">
					<Play size={12} className="animate-pulse" />
					Running
				</span>
			);
		case "waiting":
			return (
				<span className="flex items-center gap-1 bg-orange-500/10 text-orange-500 text-xs px-2 py-1 rounded-md font-medium border border-orange-500/20">
					<Clock size={12} />
					Waiting
				</span>
			);
		default:
			return (
				<span className="bg-gray-100/5 text-gray-500 text-xs px-2 py-1 rounded-md font-medium border border-border">
					No Runs
				</span>
			);
	}
}

function formatDate(date: Date | null) {
	if (!date) {
		return "N/A";
	}

	return new Intl.DateTimeFormat("en-US", {
		month: "short",
		day: "numeric",
		hour: "numeric",
		minute: "numeric",
		second: "numeric",
	}).format(date);
}

export function JobItem({ job, datasets }: JobItemProps) {
	const [showAdvanced, setShowAdvanced] = useState(false);

	const datasetName =
		datasets.find((d) => d.id === job.runsAgainst)?.name ?? "Unknown Dataset";

	const latestRun = [...(job.runs || [])].sort((a, b) => {
		const aTime = a.startedAt?.getTime() ?? 0;
		const bTime = b.startedAt?.getTime() ?? 0;

		return bTime - aTime;
	})[0];

	const { mutate: deleteJob } = useJobDeleteMutation();
	const { mutate: runJob } = useRunJobMutation();

	const handleRun = () => {
		runJob({
			profileId: job.profileId,
			jobId: job.id,
		});
	};

	const handleDelete = () => {
		deleteJob({
			profileId: job.profileId,
			jobId: job.id,
		});
	};

	return (
		<div className="border border-border rounded-md p-4 space-y-4 bg-background">
			<div className="flex items-center justify-between">
				<h3 className="font-bold text-md text-white">{job.name}</h3>

				<div className="flex items-center gap-4">
					<div className="flex items-center gap-2">
						<IconButton
							Icon={PlayIcon}
							variant="sm"
							className="text-green-500 hover:text-green-600 active:text-green-700 transition-colors hover:bg-green-500/10 rounded"
							onClick={handleRun}
						/>

						<IconButton
							Icon={Trash}
							variant="sm"
							className="text-red-500 hover:text-red-600 active:text-red-700 transition-colors hover:bg-red-500/10 rounded"
							onClick={handleDelete}
						/>
					</div>

					<StatusBadge status={latestRun?.status ?? "no_runs"} />
				</div>
			</div>

			<div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-300">
				<div>
					<span className="block text-xs font-medium text-gray-500 mb-1">
						Dataset
					</span>
					{datasetName}
				</div>
				<div>
					<span className="block text-xs font-medium text-gray-500 mb-1">
						Loss
					</span>
					{job.loss}
				</div>
				<div>
					<span className="block text-xs font-medium text-gray-500 mb-1">
						Generations
					</span>
					{job.generations}
				</div>
				<div>
					<span className="block text-xs font-medium text-gray-500 mb-1">
						Population
					</span>
					{job.population}
				</div>
				<div>
					<span className="block text-xs font-medium text-gray-500 mb-1">
						Simplify
					</span>
					{job.simplify ? "Yes" : "No"}
				</div>
				<div>
					<span className="block text-xs font-medium text-gray-500 mb-1">
						Available Functions
					</span>
					<div className="flex flex-wrap gap-2">
						{job.nonTerminals.map((fn) => (
							<span
								key={fn}
								className="bg-gray-700/50 text-gray-300 text-xs px-2 py-1 rounded-md border border-gray-600"
							>
								{fn}
							</span>
						))}
					</div>
				</div>
			</div>

			<div className="border-t border-border pt-3">
				<button
					type="button"
					onClick={() => setShowAdvanced((v) => !v)}
					className="flex items-center gap-2 text-xs font-medium text-gray-400 hover:text-gray-200 transition-colors"
				>
					{showAdvanced ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
					Advanced Settings & History
				</button>
			</div>

			{showAdvanced && (
				<div className="space-y-6 pt-2 animate-in fade-in slide-in-from-top-2 duration-200">
					<div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-400 bg-black/10 rounded-lg p-3 border border-border">
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Max Size
							</span>
							{job.maxSize ?? "N/A"}
						</div>
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Tournaments
							</span>
							{job.numberOfTournaments}
						</div>
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Crossover Prob.
							</span>
							{job.crossoverProbability}
						</div>
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Mutation Prob.
							</span>
							{job.mutationProbability}
						</div>
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Opt. Iterations
							</span>
							{job.optimizationIterations}
						</div>
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Opt. Repeats
							</span>
							{job.optimizationRepeats}
						</div>
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Max Params
							</span>
							{job.maxParamCount}
						</div>
						<div>
							<span className="block text-xs font-medium text-gray-500 mb-1">
								Split
							</span>
							{job.split}
						</div>
					</div>

					<div className="space-y-2">
						<h4 className="text-sm font-medium text-gray-300">Run History</h4>
						{job.runs && job.runs.length > 0 ? (
							<div className="border border-border rounded-lg overflow-hidden flex flex-col">
								<div className="grid grid-cols-[100px_1fr_1fr] bg-black/20 text-xs font-medium text-gray-500 px-3 py-2 border-b border-border">
									<span>Status</span>
									<span>Started</span>
									<span>Completed</span>
								</div>
								<div className="flex flex-col divide-y divide-border/50 max-h-48 overflow-y-auto">
									{[...job.runs]
										.sort((a, b) => {
											const aTime = a.startedAt?.getTime() ?? 0;
											const bTime = b.startedAt?.getTime() ?? 0;
											return bTime - aTime;
										})
										.map((run) => (
											<div
												key={run.id}
												className="grid grid-cols-[100px_1fr_1fr] px-3 py-2 text-xs items-center gap-2"
											>
												<div>
													<StatusBadge status={run.status} />
												</div>
												<span className="text-gray-400">
													{formatDate(run.startedAt)}
												</span>
												<span className="text-gray-400">
													{formatDate(run.finishedAt)}
												</span>
											</div>
										))}
								</div>
							</div>
						) : (
							<p className="text-xs text-gray-500 italic">
								This job hasn&apos;t run yet.
							</p>
						)}
					</div>
				</div>
			)}
		</div>
	);
}
