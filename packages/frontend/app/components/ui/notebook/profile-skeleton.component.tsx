import { NotebookCell } from "./cell.component";

export function ProfileSkeleton() {
	const noop = () => {};
	return (
		<div className="flex flex-col w-full divide-y divide-border animate-pulse">
			<NotebookCell
				id="skeleton-metadata"
				type="metadata"
				isActive={false}
				moveable={false}
				isDeletable={false}
				onClick={noop}
			>
				<div className="space-y-4 py-2">
					<div className="h-6 bg-white/10 rounded w-1/4" />
					<div className="h-4 bg-white/10 rounded w-3/4" />
				</div>
			</NotebookCell>
			<NotebookCell
				id="skeleton-datasets"
				type="datasets"
				isActive={false}
				moveable={false}
				isDeletable={false}
				onClick={noop}
			>
				<div className="space-y-3 py-2">
					<div className="h-4 bg-white/10 rounded w-1/5" />
					<div className="flex flex-col gap-2">
						<div className="h-10 bg-white/10 rounded w-full" />
						<div className="h-10 bg-white/10 rounded w-full" />
					</div>
				</div>
			</NotebookCell>
			<NotebookCell
				id="skeleton-jobs"
				type="jobs"
				isActive={false}
				moveable={false}
				isDeletable={false}
				onClick={noop}
			>
				<div className="space-y-3 py-2">
					<div className="h-4 bg-white/10 rounded w-1/5" />
					<div className="flex flex-col gap-2">
						<div className="h-10 bg-white/10 rounded w-full" />
						<div className="h-10 bg-white/10 rounded w-full" />
						<div className="h-10 bg-white/10 rounded w-full" />
					</div>
				</div>
			</NotebookCell>
		</div>
	);
}
