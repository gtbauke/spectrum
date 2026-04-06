import { ScatterChart as ScatterIcon, TrendingUp } from "lucide-react";
import type { Dispatch, SetStateAction } from "react";

type ModelInsightsNavigationProps = {
	activeTab: string;
	setActiveTab: Dispatch<SetStateAction<"pareto" | "validation">>;
};

export function ModelInsightsNavigation({
	activeTab,
	setActiveTab,
}: ModelInsightsNavigationProps) {
	return (
		<div className="flex px-6 border-b border-white/5 bg-white/2">
			<button
				type="button"
				onClick={() => setActiveTab("pareto")}
				className={`px-6 py-3 text-sm font-bold tracking-wide transition-all border-b-2 flex items-center gap-2 cursor-pointer ${
					activeTab === "pareto"
						? "text-primary-400 border-primary-500 bg-primary/5"
						: "text-gray-500 border-transparent hover:text-gray-300"
				}`}
			>
				<ScatterIcon size={16} /> Pareto Front
			</button>

			<button
				type="button"
				onClick={() => setActiveTab("validation")}
				className={`px-6 py-3 text-sm font-bold tracking-wide transition-all border-b-2 flex items-center gap-2 cursor-pointer ${
					activeTab === "validation"
						? "text-primary-400 border-primary-500 bg-primary/5"
						: "text-gray-500 border-transparent hover:text-gray-300"
				}`}
			>
				<TrendingUp size={16} /> Metrics
			</button>
		</div>
	);
}
