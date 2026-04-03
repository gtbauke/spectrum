import { Database, FileText, Import } from "lucide-react";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import { useActivity } from "~/contexts/activity-view.context";
import { useLinkDatasetToProfileMutation } from "~/hooks/use-link-dataset-to-profile-mutation.hook";
import type { Dataset } from "~/schemas/domain/dataset.schema";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";

type DatasetItemProps = {
	dataset: Dataset;
	active?: boolean;
};

function formatBytes(bytes: number) {
	if (bytes === 0) return "0 B";

	const k = 1024;
	const sizes = ["B", "KB", "MB", "GB", "TB"];
	const i = Math.floor(Math.log(bytes) / Math.log(k));

	return `${parseFloat((bytes / k ** i).toFixed(2))} ${sizes[i]}`;
}

export function DatasetItem({ dataset, active = false }: DatasetItemProps) {
	const tabs = useEditorStore((s) => s.tabs);
	const activeTabId = useEditorStore((s) => s.activeTabId);
	const { setActiveView } = useActivity();

	const { mutate } = useLinkDatasetToProfileMutation();

	const mainArtifact = dataset.artifacts.find(
		(a) => a.role === "data" || a.role === "validation",
	);

	const type = mainArtifact?.path.endsWith(".csv") ? "CSV" : "FILE";
	const size = formatBytes(
		dataset.artifacts.reduce((acc, artifact) => acc + artifact.sizeInBytes, 0),
	);

	const onImportIconClick = () => {
		const isActiveTabProfile = activeTabId
			? tabs[activeTabId].type === "profile"
			: false;

		if (isActiveTabProfile) {
			mutate({
				profile: { id: activeTabId! },
				data: {
					dataset_ids: [dataset.id],
				},
			});

			return;
		}

		mutate(
			{
				profile: {
					name: `Profile for ${dataset.name}`,
					description: `Auto-generated profile for dataset ${dataset.name}`,
				},
				data: {
					dataset_ids: [dataset.id],
				},
			},
			{
				onSuccess: () => {
					setActiveView("profiles");
				},
			},
		);
	};

	return (
		<div className="flex flex-col">
			<div
				className={cn(
					"group flex items-center justify-between p-2 rounded-md cursor-pointer transition-colors",
					active
						? "bg-primary-500/10 text-white"
						: "text-gray-400 hover:bg-white/5 hover:text-gray-200",
				)}
			>
				<div className="flex items-center gap-3 truncate">
					{type === "CSV" ? (
						<Database size={14} className="text-blue-400" />
					) : (
						<FileText size={14} className="text-orange-400" />
					)}
					<div className="flex flex-col truncate items-start text-left">
						<span className="text-xs font-medium truncate">{dataset.name}</span>
						<span className="text-[10px] text-gray-600">
							{size} • {type}
						</span>
					</div>
				</div>

				<IconButton
					Icon={Import}
					variant="sm"
					className="hover:text-primary-500 hover:bg-primary-500/10"
					onClick={onImportIconClick}
				/>
			</div>
		</div>
	);
}
