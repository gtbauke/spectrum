import * as katex from "react-katex";
import type { ModelMetricsParetoFront } from "~/schemas/domain/model.schema";

type ModelInsightsExpressionListProps = {
	paretoFront?: ModelMetricsParetoFront[];
};

export function ModelInsightsExpressionList({
	paretoFront,
}: ModelInsightsExpressionListProps) {
	return (
		<div className="flex-1 bg-white/3 border border-white/5 rounded-2xl flex flex-col">
			<div className="px-5 py-4 border-b border-white/5 bg-white/2 rounded-t-2xl flex items-center justify-between">
				<h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2">
					Pareto Models
				</h3>
				<span className="text-[10px] bg-white/10 px-2 py-0.5 rounded-full text-gray-400">
					{paretoFront?.length || 0} Expressions
				</span>
			</div>

			<div className="flex-1 overflow-y-auto custom-scrollbar p-2">
				{!paretoFront && (
					<div className="flex-1 flex items-center justify-center">
						<p className="text-gray-500 text-sm">
							No metrics available for this model.
						</p>
					</div>
				)}

				<div className="space-y-1">
					{paretoFront?.map((item, idx) => (
						<div
							key={idx.toString()}
							className="p-4 rounded-xl border border-transparent hover:border-white/10 hover:bg-white/5 transition-all group relative cursor-default"
						>
							<div className="flex justify-between items-start mb-2">
								<span className="text-[10px] font-mono text-gray-500">
									ID: {item.id}
								</span>
								<div className="flex gap-3 text-[10px] font-bold text-gray-400">
									<span>Fitness: {item?.fitness?.toFixed(4)}</span>
									<span>Size: {item.size}</span>
								</div>
							</div>
							<div className="font-mono text-xs text-primary-400 line-clamp-2 break-all bg-black/30 px-2 rounded-lg border border-white/5">
								<katex.BlockMath math={item.latex} />
							</div>
						</div>
					))}
				</div>
			</div>
		</div>
	);
}
