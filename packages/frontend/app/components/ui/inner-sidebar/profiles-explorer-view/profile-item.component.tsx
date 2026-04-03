import { motion } from "framer-motion";
import { Globe, Layout, Lock, MoreVertical } from "lucide-react";
import type { Profile } from "~/schemas/domain/profile.schema";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";

type ProfileItemProps = {
	profile: Profile;
	active?: boolean;
};

export function ProfileItem({ profile, active = false }: ProfileItemProps) {
	const openTab = useEditorStore((s) => s.openTab);

	const handleOnDoubleClick = () => {
		openTab({
			type: "profile",
			id: profile.id,
			data: {
				tabId: profile.id,
				blocks: [],
				isDirty: false,
				future: [],
				past: [],
				activeBlockId: null,
				profileId: profile.id,
				versionId: profile.id, // Using profile ID as version ID for now
			},
		});
	};

	const isPublic = profile.mode === "released";

	return (
		<div className="flex flex-col">
			{/** biome-ignore lint/a11y/useSemanticElements: Must use div for custom button behavior */}
			<div
				role="button"
				tabIndex={0}
				onClick={handleOnDoubleClick}
				onDoubleClick={handleOnDoubleClick}
				className={cn(
					"group flex items-center justify-between p-2 rounded-md cursor-pointer transition-colors outline-none focus-visible:ring-2 focus-visible:ring-primary-500/50",
					active
						? "bg-primary-500/10 text-white"
						: "text-gray-400 hover:bg-white/5 hover:text-gray-200",
				)}
				onKeyDown={(e) => {
					if (e.key === "Enter" || e.key === " ") {
						e.preventDefault();
						handleOnDoubleClick();
					}
				}}
			>
				<div className="flex items-center gap-2 truncate">
					<div className="relative">
						<Layout size={14} className="text-primary-400 shrink-0" />
					</div>

					<div className="flex flex-col truncate items-start">
						<div className="flex items-center gap-2">
							<span className="text-xs font-medium truncate text-gray-200">
								{profile.name}
							</span>
							{isPublic ? (
								<Globe size={12} className="text-blue-400" />
							) : (
								<Lock size={12} className="text-amber-400" />
							)}
						</div>
					</div>
				</div>

				<button
					type="button"
					className="opacity-0 group-hover:opacity-100 p-1 text-gray-500 hover:bg-white/5 hover:text-gray-200 transition-colors cursor-pointer rounded"
				>
					<MoreVertical size={14} />
				</button>
			</div>
		</div>
	);
}
