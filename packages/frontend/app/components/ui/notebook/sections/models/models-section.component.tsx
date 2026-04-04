import type { Job } from "~/schemas/domain/job.schema";
import type { Model } from "~/schemas/domain/model.schema";
import { ModelItem } from "./model-item.component";

type ProfileModelsSectionProps = {
	models: Model[];
	jobs: Job[];
};

export function ProfileModelsSection({
	models,
	jobs,
}: ProfileModelsSectionProps) {
	const findJobName = (generatedBy: string) => {
		const job = jobs.find((job) => job.id === generatedBy);
		return job ? job.name : "Unknown Job";
	};

	return (
		<div className="bg-background-surface border border-border rounded-lg p-5 shadow-sm space-y-4">
			<div className="flex items-center justify-between">
				<div className="flex flex-col gap-1">
					<h2 className="text-xl font-bold text-foreground">Models</h2>
					<p className="text-xs text-muted-foreground">
						Discovered expressions and graph structures from your jobs.
					</p>
				</div>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
				{models.length === 0 ? (
					<div className="col-span-full py-8 border border-dashed border-border rounded-lg flex flex-col items-center justify-center bg-white/5 opacity-50">
						<span className="text-sm text-muted-foreground font-medium">
							No models discovered yet.
						</span>
						<span className="text-[10px] text-muted-foreground/60 mt-1 uppercase tracking-widest font-bold">
							Run a job to generate models
						</span>
					</div>
				) : (
					models.map((model) => (
						<ModelItem
							key={model.id}
							model={model}
							jobName={findJobName(model.generatedBy)}
						/>
					))
				)}
			</div>
		</div>
	);
}
