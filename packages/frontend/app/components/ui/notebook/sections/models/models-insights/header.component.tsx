import { Activity, X } from "lucide-react";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import type { Model } from "~/schemas/domain/model.schema";

type ModelInsightsHeaderProps = {
	model: Model;
	onClose: () => void;
};

export function ModelInsightsHeader({
	model,
	onClose,
}: ModelInsightsHeaderProps) {
	return (
		<div className="flex items-center justify-between px-6 py-3 border-b border-white/5 bg-linear-to-r from-primary/10 to-transparent">
			<div className="flex items-center gap-4">
				<div className="p-2.5 bg-primary/20 rounded-xl text-primary-400 border border-primary/20">
					<Activity size={20} className="animate-pulse" />
				</div>
				<div>
					<h2 className="text-lg font-bold text-white tracking-tight">
						{model.name}
					</h2>
					<div className="flex items-center gap-2">
						<span className="text-[10px] uppercase tracking-wider font-bold text-gray-500">
							ID: {model.id}
						</span>
					</div>
				</div>
			</div>

			<IconButton
				Icon={X}
				aria-label="Close insights"
				onClick={onClose}
				variant="sm"
				className="p-1.5 hover:bg-white/10 rounded-md text-primary-400 hover:text-primary-300 transition-all flex items-center gap-1.5 cursor-pointer"
			/>
		</div>
	);
}
