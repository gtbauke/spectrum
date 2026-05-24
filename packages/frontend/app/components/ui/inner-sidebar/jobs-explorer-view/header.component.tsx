import type { ProfileFilter } from "~/schemas/dtos/profile.dto";
import { cn } from "~/utils/classname.util";
import { SidebarSearchInput } from "../searchbar.component";
import { SidebarTitle } from "../title.component";

type HeaderProps = {
	className?: string;
	filters: ProfileFilter;
	onFiltersChange: (filters: ProfileFilter) => void;
};

export function Header({ className, filters, onFiltersChange }: HeaderProps) {
	const activeFilterCount = Object.entries(filters).filter(
		([, val]) => val !== "" && val !== false,
	).length;

	const updateFilter = <TKey extends keyof ProfileFilter>(
		key: TKey,
		value: ProfileFilter[TKey],
	) => {
		onFiltersChange({ ...filters, [key]: value });
	};

	return (
		<div
			className={cn(
				"flex flex-col border-b border-white/5 shrink-0",
				className,
			)}
		>
			<div className="p-4 pb-3 space-y-3">
				<SidebarTitle activeFilterCount={activeFilterCount}>
					Jobs Search
				</SidebarTitle>

				<SidebarSearchInput
					type="text"
					search={filters.name || ""}
					onSearchChange={(value) => updateFilter("name", value)}
					placeholder="Search by profile name..."
				/>
			</div>
		</div>
	);
}
