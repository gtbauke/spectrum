import { Globe, Layout, Lock, Trash } from "lucide-react";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import { useProfileDeleteMutation } from "~/hooks/use-profile-delete-mutation.hook";
import { useProfileQueryState } from "~/hooks/use-profile-query-state.hook";
import type { ProfileSummary } from "~/schemas/domain/profile.schema";
import { cn } from "~/utils/classname.util";

type ProfileItemProps = {
	profile: ProfileSummary;
	active?: boolean;
	lastUpdated?: Date | null;
};

function formatRelativeTime(lastUpdatedDate: Date) {
	const now = new Date();
	const diffInSeconds = Math.floor(
		(now.getTime() - lastUpdatedDate.getTime()) / 1000,
	);

	if (diffInSeconds < 60) {
		return `${diffInSeconds} seconds ago`;
	} else if (diffInSeconds < 3600) {
		const minutes = Math.floor(diffInSeconds / 60);
		return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
	} else if (diffInSeconds < 86400) {
		const hours = Math.floor(diffInSeconds / 3600);
		return `${hours} hour${hours > 1 ? "s" : ""} ago`;
	}

	const days = Math.floor(diffInSeconds / 86400);
	return `${days} day${days > 1 ? "s" : ""} ago`;
}

export function ProfileItem({
	profile,
	active = false,
	lastUpdated = null,
}: ProfileItemProps) {
	const { openTab } = useProfileQueryState();
	const { mutate: deleteProfile } = useProfileDeleteMutation();

	const handleOnDoubleClick = () => {
		openTab(profile.id, profile.name);
	};

	const isPublic = profile.mode === "released";

	const handleDeleteClick = (e: React.MouseEvent<HTMLButtonElement>) => {
		e.stopPropagation();
		deleteProfile(profile.id);
	};

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
						<Layout size={16} className="text-primary-400 shrink-0" />
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

				{lastUpdated ? (
					<span className="text-xs text-gray-500">
						{formatRelativeTime(lastUpdated)}
					</span>
				) : (
					<IconButton
						Icon={Trash}
						variant="sm"
						className="opacity-0 group-hover:opacity-100 p-1 text-gray-500 hover:bg-red-500/10 hover:text-red-500 transition-colors cursor-pointer rounded"
						onClick={handleDeleteClick}
					/>
				)}
			</div>
		</div>
	);
}
