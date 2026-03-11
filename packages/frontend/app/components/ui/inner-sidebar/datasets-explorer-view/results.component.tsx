import { useDatasets } from "~/hooks/use-datasets.hook";
import type { Dataset } from "~/schemas/generated/dataset.schema";
import { DatasetItem } from "./dataset-item.component";

type ResultsProps = {
    search: string;
    page: number;
    onPageChange: (page: number | ((p: number) => number)) => void;
};

export function Results({ search, page, onPageChange }: ResultsProps) {
    const { data, isLoading, isPlaceholderData } = useDatasets(
        { name: search },
        page,
    );

    if (isLoading) {
        return <div className="p-4 text-xs text-gray-500">Loading datasets...</div>;
    }

    return (
        <div className="flex-1 overflow-y-auto custom-scrollbar space-y-6">
            <section className="h-full flex flex-col justify-between">
                <div className="p-2">
                    <h3 className="px-2 mb-2 text-[9px] font-bold text-gray-600 uppercase">
                        Recent
                    </h3>
                    <div className="space-y-1">
                        {data?.items.map((dataset: Dataset) => {
                            return (
                                <DatasetItem
                                    key={dataset.id}
                                    dataset={dataset}
                                />
                            );
                        })}
                    </div>
                </div>

                <div className="p-2 flex items-center justify-between border-t border-white/5 bg-black/20">
                    <button
                        type="button"
                        disabled={page === 1 || isPlaceholderData}
                        onClick={() => onPageChange((p) => p - 1)}
                        className="text-[10px] uppercase font-bold text-gray-500 hover:text-white disabled:hover:text-gray-500 disabled:opacity-30 cursor-pointer disabled:cursor-not-allowed"
                    >
                        Prev
                    </button>
                    <span className="text-[10px] text-gray-600">
                        Page {data?.page} of {data?.pages}
                    </span>
                    <button
                        type="button"
                        disabled={page >= (data?.pages ?? 1) || isPlaceholderData}
                        onClick={() => onPageChange((p) => p + 1)}
                        className="text-[10px] uppercase font-bold text-gray-500 hover:text-white disabled:hover:text-gray-500 disabled:opacity-30 cursor-pointer disabled:cursor-not-allowed"
                    >
                        Next
                    </button>
                </div>
            </section>
        </div>
    );
}
