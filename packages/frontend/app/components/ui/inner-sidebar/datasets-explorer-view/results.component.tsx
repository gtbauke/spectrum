import { useEffect } from "react";
import type { DatasetFilters } from "~/api/datasets.api";
import { useInfiniteDatasets } from "~/hooks/use-datasets.hook";
import { useIntersection } from "~/hooks/use-intersection.hook";
import type { Dataset } from "~/schemas/models/dataset.schema";
import { DatasetItem } from "./dataset-item.component";

type ResultsProps = {
	filters: DatasetFilters;
};

export function Results({ filters }: ResultsProps) {
	const { data, isLoading, isFetchingNextPage, hasNextPage, fetchNextPage } =
		useInfiniteDatasets(filters);

	const { ref, isIntersecting } = useIntersection<HTMLDivElement>();

	useEffect(() => {
		if (isIntersecting && hasNextPage && !isFetchingNextPage) {
			fetchNextPage();
		}
	}, [isIntersecting, fetchNextPage, hasNextPage, isFetchingNextPage]);

	if (isLoading) {
		return (
			<div className="p-4 text-xs text-gray-500 animate-pulse">
				Loading datasets...
			</div>
		);
	}

	const datasets = data?.pages.flatMap((page) => page.items) || [];

	return (
		<div className="flex-1 flex flex-col overflow-hidden">
			<div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
				{datasets.map((dataset: Dataset) => {
					return <DatasetItem key={dataset.id} dataset={dataset} />;
				})}
			</div>

			<div ref={ref} className="h-4 w-full shrink-0" aria-hidden="true" />

			{isFetchingNextPage && (
				<div className="py-2 text-center text-[10px] text-gray-500 font-medium uppercase tracking-wider animate-pulse">
					Loading more...
				</div>
			)}

			{!hasNextPage && datasets.length > 0 && (
				<div className="py-4 text-center text-[10px] text-gray-600 font-medium">
					End of results
				</div>
			)}
		</div>
	);
}
