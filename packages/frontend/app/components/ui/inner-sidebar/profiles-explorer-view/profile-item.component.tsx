import { AnimatePresence, motion } from "framer-motion";
import {
	ChevronRight,
	Globe,
	History,
	Layout,
	Lock,
	MoreVertical,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import type { Profile } from "~/schemas/models/profile.schema";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";

type ProfileItemProps = {
	profile: Profile;
	active?: boolean;
};

export function ProfileItem({ profile, active = false }: ProfileItemProps) {
	const [isOpen, setIsOpen] = useState(false);
	const openTab = useEditorStore((s) => s.openTab);

	const clickTimeoutRef = useRef<NodeJS.Timeout | null>(null);

	useEffect(() => {
		return () => {
			if (clickTimeoutRef.current) {
				clearTimeout(clickTimeoutRef.current);
			}
		};
	}, []);

	const latestVersion =
		profile.versions.find((v) => v.is_latest) || profile.versions[0];

	if (!latestVersion) {
		return null;
	}

	const isPublic = latestVersion.visibility === "public";
	const isActive = latestVersion.status === "active";

	const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
		if (e.key === "Enter" || e.key === " ") {
			e.preventDefault();
			setIsOpen((prev) => !prev);
		}
	};

	const handleSingleClick = (e: React.MouseEvent) => {
		if (clickTimeoutRef.current) {
			clearTimeout(clickTimeoutRef.current);
		}

		if (e.detail === 1) {
			clickTimeoutRef.current = setTimeout(() => {
				setIsOpen((prev) => !prev);
			}, 100);
		}
	};

	const handleOnDoubleClick = () => {
		if (clickTimeoutRef.current) {
			clearTimeout(clickTimeoutRef.current);
		}

		openTab({
			type: "profile",
			id: profile.id,
			data: {
				tabId: profile.id,
				name: latestVersion.name,
				blocks: [],
				isDirty: false,
				future: [],
				past: [],
				activeBlockId: null,
				profileId: profile.id,
				versionId: latestVersion.id,
				description: latestVersion.description || null,
			},
		});
	};

	return (
		<div className="flex flex-col">
			{/** biome-ignore lint/a11y/useSemanticElements: Cannot have nested buttons */}
			<div
				role="button"
				tabIndex={0}
				aria-expanded={isOpen}
				onClick={handleSingleClick}
				onKeyDown={handleKeyDown}
				onDoubleClick={handleOnDoubleClick}
				className={cn(
					"group flex items-center justify-between p-2 rounded-md cursor-pointer transition-colors outline-none focus-visible:ring-2 focus-visible:ring-primary-500/50",
					active
						? "bg-primary-500/10 text-white"
						: "text-gray-400 hover:bg-white/5 hover:text-gray-200",
				)}
			>
				<div className="flex items-center gap-2 truncate">
					<motion.div
						animate={{ rotate: isOpen ? 90 : 0 }}
						transition={{ duration: 0.2, ease: "easeInOut" }}
					>
						<ChevronRight size={12} />
					</motion.div>

					<div className="relative">
						<Layout size={14} className="text-primary-400 shrink-0" />
						<span
							className={cn(
								"absolute -bottom-0.5 -right-0.5 w-1.5 h-1.5 rounded-full border border-[#111319]",
								isActive ? "bg-emerald-500" : "bg-red-500",
							)}
						/>
					</div>

					<div className="flex flex-col truncate items-start">
						<div className="flex items-center gap-2">
							<span className="text-xs font-medium truncate text-gray-200">
								{latestVersion.name}
							</span>
							{isPublic ? (
								<Globe size={12} className="text-blue-400" />
							) : (
								<Lock size={12} className="text-amber-400" />
							)}
						</div>
						<span className="text-[10px] text-gray-600">
							{profile.versions.length} versions
						</span>
					</div>
				</div>

				<button
					type="button"
					className="opacity-0 group-hover:opacity-100 p-1 text-gray-500 hover:bg-white/5 hover:text-gray-200 transition-colors cursor-pointer"
				>
					<MoreVertical size={14} />
				</button>
			</div>

			<AnimatePresence initial={false}>
				{isOpen && (
					<motion.div
						initial={{ height: 0, opacity: 0 }}
						animate={{ height: "auto", opacity: 1 }}
						exit={{ height: 0, opacity: 0 }}
						transition={{ duration: 0.3, ease: [0.04, 0.62, 0.23, 0.98] }}
						className="overflow-hidden"
					>
						<div className="ml-7 mt-1 border-l border-border space-y-1">
							{profile.versions.map((version, index) => (
								<motion.div
									key={version.id}
									initial={{ x: -10, opacity: 0 }}
									animate={{ x: 0, opacity: 1 }}
									transition={{ delay: index * 0.05 }}
									className="group/version flex flex-col p-1.5 pl-3 text-[10px] text-gray-500 hover:text-gray-300 hover:bg-white/5 rounded-r-sm cursor-pointer"
								>
									<div className="flex items-center gap-2">
										<History size={10} />
										<span>v{version.version}</span>
										<span className="text-gray-600 truncate ml-1">
											{new Date(version.timestamp).toLocaleDateString()}
										</span>
										{version.is_latest && (
											<span className="ml-auto text-[8px] bg-emerald-500/10 text-secondary-500 px-1 rounded uppercase font-bold tracking-wider">
												Latest
											</span>
										)}
									</div>

									<div className="pl-4 mt-0.5 text-[9px] text-gray-600 opacity-0 group-hover/version:opacity-100 transition-opacity">
										{version.datasets?.length || 0} datasets attached
									</div>
								</motion.div>
							))}
						</div>
					</motion.div>
				)}
			</AnimatePresence>
		</div>
	);
}
