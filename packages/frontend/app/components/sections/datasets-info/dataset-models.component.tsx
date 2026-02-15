import { ModelCard } from "~/components/ui/model-card/model-card.component";
import { Section } from "~/components/ui/section.component";
import type { Model } from "~/schemas/model.schema";

type DatasetModelsProps = {
	models: Model[];
};

export function DatasetModels({ models }: DatasetModelsProps) {
	if (models.length === 0) {
		return (
			<Section title="Models">
				<p className="text-gray-600">No models found for this dataset.</p>
			</Section>
		);
	}

	return (
		<Section title="Models">
			{models.map((model) => (
				<ModelCard key={model.id} model={model} />
			))}
		</Section>
	);
}
