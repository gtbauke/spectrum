import { AnimatePresence, motion } from "framer-motion";
import { FilterX } from "lucide-react";
import type { ProfileFilter } from "~/schemas/dtos/profile.dto";
import { Field } from "~/components/ui/forms/field/field.component";
import { SelectInput } from "~/components/ui/forms/input/select-input.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { ToggleInput } from "~/components/ui/forms/input/toggle-input.component";
import { profileModeSchema } from "~/schemas/domain/enums.schema";
import { capitalize } from "~/utils/capitalize.util";
import { validateEnum } from "~/utils/validate-enum.util";

type ProfilesAdvancedFiltersProps = {
	isAdvancedFilterOpen: boolean;
	activeFilterCount: number;
	filters: ProfileFilter;
	updateFilter: <TKey extends keyof ProfileFilter>(
		key: TKey,
		value: ProfileFilter[TKey],
	) => void;
	clearFilters: () => void;
};

export function ProfilesAdvancedFilters({
	activeFilterCount,
	filters,
	isAdvancedFilterOpen,
	updateFilter,
	clearFilters,
}: ProfilesAdvancedFiltersProps) {
	return (
		<AnimatePresence initial={false}>
			{isAdvancedFilterOpen && (
				<motion.div
					initial={{ height: 0, opacity: 0 }}
					animate={{ height: "auto", opacity: 1 }}
					exit={{ height: 0, opacity: 0 }}
					transition={{ duration: 0.2, ease: "easeInOut" }}
					className="overflow-hidden bg-black/20 border-t border-white/5"
				>
					<div className="p-4 space-y-3">
						<div className="flex items-center justify-between mb-1">
							<span className="text-[10px] uppercase font-bold tracking-wider text-gray-500">
								Advanced Filters
							</span>

							{activeFilterCount > 0 && (
								<button
									type="button"
									onClick={clearFilters}
									className="text-[10px] text-gray-400 hover:text-red-400 flex items-center gap-1 transition-colors cursor-pointer"
								>
									<FilterX size={10} /> Clear
								</button>
							)}
						</div>

						<div className="space-y-3 flex flex-col">
							<Field>
								<Field.Label className="text-[10px]">Name</Field.Label>
								<Field.Control>
									<TextInput
										placeholder="Filter by name..."
										value={filters.name || ""}
										onChange={(e) => updateFilter("name", e.target.value)}
										className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
									/>
								</Field.Control>
							</Field>

							<Field>
								<Field.Label className="text-[10px]">Description</Field.Label>
								<Field.Control>
									<TextAreaInput
										placeholder="Filter by description..."
										value={filters.description || ""}
										onChange={(e) => updateFilter("description", e.target.value)}
										className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
									/>
								</Field.Control>
							</Field>

							<Field>
								<Field.Label className="text-[10px]">Mode</Field.Label>
								<Field.Control>
									<SelectInput
										value={filters.status}
										onChange={(e) =>
											updateFilter(
												"status",
												validateEnum(e.target.value, profileModeSchema),
											)
										}
										options={profileModeSchema.options.map((mode) => ({
											label: capitalize(mode),
											value: mode,
										}))}
										className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
									/>
								</Field.Control>
							</Field>

							<Field>
								<Field.Control>
									<ToggleInput
										checked={filters.onlyMe || false}
										onChange={(e) => updateFilter("onlyMe", e.target.checked)}
									/>
									<Field.Label className="text-[10px] ml-3 mt-0.5">Authored by me</Field.Label>
								</Field.Control>
							</Field>
						</div>
					</div>
				</motion.div>
			)}
		</AnimatePresence>
	);
}
