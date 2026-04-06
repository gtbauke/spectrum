import ReactECharts from "echarts-for-react";
import { Activity, Check, TrendingUp } from "lucide-react";
import { useMemo, useState } from "react";
import { useModelValidation } from "~/hooks/use-model-validation.hook";
import type { Model } from "~/schemas/domain/model.schema";
import { ModelInsightsExpressionList } from "./models-insights/expressions.component";
import { ModelInsightsHeader } from "./models-insights/header.component";
import { ModelInsightsNavigation } from "./models-insights/navigation.component";

type ModelInsightsProps = {
	model: Model;
	onClose: () => void;
};

export function ModelInsights({ model, onClose }: ModelInsightsProps) {
	const [activeTab, setActiveTab] = useState<"pareto" | "validation">("pareto");
	const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());

	const { data: validationData, isLoading } = useModelValidation<
		{ actual: number; [key: string]: number }[]
	>({
		modelId: model.id,
		validationPath: model.validationPath,
	});

	const toggleSelection = (id: number) => {
		const newSet = new Set(selectedIds);

		if (newSet.has(id)) {
			newSet.delete(id);
		} else {
			if (newSet.size < 5) {
				newSet.add(id);
			}
		}

		setSelectedIds(newSet);
	};

	const paretoOption = useMemo(() => {
		const scatterData = model.metrics?.paretoFront
			.filter((item) => item.size > 1)
			.map((item) => [item.size, item.fitness, item.numpy]);

		return {
			backgroundColor: "transparent",
			tooltip: {
				trigger: "item",
				backgroundColor: "rgba(0, 0, 0, 0.8)",
				borderColor: "#333",
				textStyle: { color: "#fff" },
				formatter: (params: { data: [number, number, string] }) => `
					<div class="p-2">
						<div class="text-[10px] text-gray-400 font-bold uppercase mb-1">Pareto Expression</div>
						<div class="text-xs font-mono text-primary-400 mb-2">${params?.data?.[2] || "N/A"}</div>
						<div class="flex justify-between gap-4">
							<span class="text-gray-500">Size:</span>
							<span class="font-mono">${params?.data?.[0] || "N/A"}</span>
						</div>
						<div class="flex justify-between gap-4">
							<span class="text-gray-500">Fitness:</span>
							<span class="font-mono">${params?.data?.[1]?.toFixed(5) || "N/A"}</span>
						</div>
					</div>
				`,
			},
			grid: { top: 40, right: 30, bottom: 50, left: 60 },
			xAxis: {
				name: "Size",
				nameLocation: "middle",
				nameGap: 30,
				type: "value",
				splitLine: { lineStyle: { color: "#222" } },
				axisLine: { lineStyle: { color: "#444" } },
			},
			yAxis: {
				name: "Fitness",
				nameLocation: "middle",
				nameGap: 45,
				type: "value",
				splitLine: { lineStyle: { color: "#222" } },
				axisLine: { lineStyle: { color: "#444" } },
				min: (value: { max: number; min: number }) => {
					const padding = (value.max - value.min) * 0.5;
					return value.min - padding;
				},
				max: (value: { max: number; min: number }) => {
					const padding = (value.max - value.min) * 0.5;
					return value.max + padding;
				},
			},
			series: [
				{
					data: scatterData,
					type: "scatter",
					symbolSize: 12,
					itemStyle: {
						color: "#7c3aed",
					},
					emphasis: {
						itemStyle: {
							color: "#6928d9",
							scale: 1.5,
						},
					},
				},
			],
		};
	}, [model.metrics?.paretoFront]);

	const validationOption = useMemo(() => {
		if (!validationData || validationData.length === 0) {
			return {};
		}

		const series = [];
		const actualY = validationData.map((d) => d.actual);

		series.push({
			name: "Target (Actual)",
			type: "line",
			data: actualY,
			symbol: "none",
			lineStyle: { width: 3, color: "#10b981" },
			z: 10,
		});

		const colors = ["#3b82f6", "#f59e0b", "#ec4899", "#8b5cf6", "#06b6d4"];

		Array.from(selectedIds).forEach((id, i) => {
			const item = model.metrics?.paretoFront.find((p) => p.id === id);
			if (!item) {
				return;
			}

			const exprKey = `model_${id}`;
			series.push({
				name: `Model #${id}`,
				type: "line",
				data: validationData.map((d) => d[exprKey]),
				symbol: "none",
				smooth: true,
				lineStyle: {
					width: 2,
					type: "dashed",
					color: colors[i % colors.length],
				},
				opacity: 0.8,
				z: 11,
			});
		});

		return {
			backgroundColor: "transparent",
			tooltip: {
				trigger: "axis",
				backgroundColor: "rgba(0, 0, 0, 0.8)",
				borderColor: "#333",
				textStyle: { color: "#fff" },
			},
			legend: {
				data: series.map((s) => s.name),
				bottom: 0,
				textStyle: { color: "#9ca3af", fontSize: 10 },
			},
			grid: { top: 40, right: 30, bottom: 80, left: 60 },
			xAxis: { type: "category", splitLine: { show: false } },
			yAxis: { type: "value", splitLine: { lineStyle: { color: "#222" } } },
			series,
		};
	}, [validationData, selectedIds, model.metrics?.paretoFront]);

	return (
		<div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-300">
			<div className="bg-[#0a0a0a] border border-white/10 rounded-2xl w-full max-w-6xl max-h-[85vh] flex flex-col">
				<ModelInsightsHeader model={model} onClose={onClose} />
				<ModelInsightsNavigation
					activeTab={activeTab}
					setActiveTab={setActiveTab}
				/>

				<div className="flex-1 overflow-scroll overflow-x-hidden flex flex-col p-6">
					{activeTab === "pareto" ? (
						<div className="flex-1 flex flex-col lg:flex-row gap-6">
							<div className="flex-2 self-start bg-white/3 border border-white/5 rounded-2xl p-6 relative group">
								<div className="relative">
									<ReactECharts
										option={paretoOption}
										style={{ width: "100%" }}
									/>
								</div>
							</div>

							<ModelInsightsExpressionList
								paretoFront={model.metrics?.paretoFront}
							/>
						</div>
					) : (
						<div className="flex-1 flex flex-col lg:flex-row gap-6">
							<div className="w-full lg:w-80 bg-white/3 border border-white/5 rounded-2xl flex flex-col">
								<div className="px-5 py-4 border-b border-white/5 bg-white/2">
									<h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest">
										Select to Compare
									</h3>
									<p className="text-[10px] text-gray-500 mt-1">
										Comparison overlay (max 5 models)
									</p>
								</div>
								<div className="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-2">
									{model.metrics?.paretoFront.map((item) => (
										<button
											type="button"
											key={item.id.toString()}
											onClick={() => toggleSelection(item.id)}
											className={`w-full text-left p-3 rounded-xl border transition-all flex items-center justify-between group cursor-pointer ${
												selectedIds.has(item.id)
													? "bg-primary/10 border-primary-500/50"
													: "bg-white/5 border-transparent hover:border-white/10"
											}`}
										>
											<div>
												<div className="text-[10px] font-bold text-gray-500 mb-1">
													MODEL #{item.id}
												</div>
												<div className="text-xs font-mono text-white truncate max-w-37.5">
													{item.numpy}
												</div>
											</div>
											<div
												className={`w-5 h-5 rounded-lg border flex items-center justify-center transition-all ${
													selectedIds.has(item.id)
														? "bg-primary-500 border-primary-500 text-white"
														: "border-white/10 bg-black/20"
												}`}
											>
												{selectedIds.has(item.id) && (
													<Check size={14} strokeWidth={3} />
												)}
											</div>
										</button>
									))}
								</div>
							</div>

							<div className="flex-1 bg-white/3 border border-white/5 rounded-2xl p-6 flex flex-col">
								{isLoading ? (
									<div className="flex-1 flex flex-col items-center justify-center gap-4">
										<Activity
											size={40}
											className="text-primary-500 animate-spin"
										/>
										<p className="text-gray-500 font-bold uppercase tracking-widest text-xs">
											Decoding Validation Cache...
										</p>
									</div>
								) : validationData && validationData.length > 0 ? (
									<div className="flex-1 h-full">
										<ReactECharts
											option={validationOption}
											style={{ height: "100%", width: "100%" }}
										/>
									</div>
								) : (
									<div className="flex-1 flex flex-col items-center justify-center gap-4 text-center">
										<TrendingUp size={40} className="text-gray-700" />
										<div>
											<p className="text-gray-400 font-bold uppercase tracking-widest text-xs">
												No Sample Data
											</p>
											<p className="text-gray-600 text-[10px] mt-1 max-w-50">
												Validation results are either empty or currently being
												computed by the worker.
											</p>
										</div>
									</div>
								)}
							</div>
						</div>
					)}
				</div>
			</div>
		</div>
	);
}
