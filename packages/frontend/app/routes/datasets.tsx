import { getAllDatasets } from "~/api/get-all-datasets.api";
import { MainContainer } from "~/components/layout/main.component";
import { DatasetCard } from "~/components/ui/dataset-card/card.component";
import type { Route } from "./+types/datasets";

export async function clientLoader() {
	const response = await getAllDatasets();
	return response;
}

export function HydrateFallback() {
	return (
		<MainContainer>
			<h1>Loading datasets...</h1>
		</MainContainer>
	);
}

export default function DatasetsScreen({ loaderData }: Route.ComponentProps) {
	return (
		<MainContainer>
			<div className="space-y-6">
				<h1 className="text-2xl font-bold">Datasets</h1>

				<ul className="container mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
					{loaderData.map((dataset) => (
						<li key={dataset.id}>
							<DatasetCard dataset={dataset} />
						</li>
					))}
				</ul>
			</div>
		</MainContainer>
	);
}
