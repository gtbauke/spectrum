import { AnimatePresence, motion } from "framer-motion";
import { FilterX } from "lucide-react";
import type { ProfileFilters } from "~/api/profiles.api";
import { SelectInput } from "~/components/ui/forms/input/select-input.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { ToggleInput } from "~/components/ui/forms/input/toggle-input.component";
import {
    profileDatasetRoleSchema,
    profileDatasetRoleValues,
} from "~/schemas/generated/profile-dataset-role.schema";
import {
    profileStatusSchema,
    profileStatusValues,
} from "~/schemas/generated/profile-status.schema";
import {
    profileVisibilitySchema,
    profileVisibilityValues,
} from "~/schemas/generated/profile-visibility.schema";
import { capitalize } from "~/utils/capitalize.util";
import { validateEnum } from "~/utils/validate-enum.util";

type ProfilesAdvancedFiltersProps = {
    isAdvancedFilterOpen: boolean;
    activeFilterCount: number;
    filters: ProfileFilters;
    updateFilter: <TKey extends keyof ProfileFilters>(
        key: TKey,
        value: ProfileFilters[TKey],
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
                            <TextAreaInput
                                label="Description"
                                placeholder="Filter by description..."
                                value={filters.description}
                                onChange={(e) => updateFilter("description", e.target.value)}
                                className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
                                labelClassName="text-[10px]"
                            />

                            <TextInput
                                label="Version"
                                type="number"
                                placeholder="e.g. 1"
                                value={filters.version}
                                onChange={(e) =>
                                    updateFilter(
                                        "version",
                                        e.target.value ? Number(e.target.value) : undefined,
                                    )
                                }
                                className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
                                labelClassName="text-[10px]"
                            />

                            <SelectInput
                                label="Status"
                                value={filters.status}
                                onChange={(e) =>
                                    updateFilter(
                                        "status",
                                        validateEnum(e.target.value, profileStatusSchema),
                                    )
                                }
                                options={profileStatusValues.map((status) => ({
                                    label: capitalize(status),
                                    value: status,
                                }))}
                                className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
                                labelClassName="text-[10px]"
                            />

                            <SelectInput
                                label="Visibility"
                                value={filters.visibility}
                                onChange={(e) =>
                                    updateFilter(
                                        "visibility",
                                        validateEnum(e.target.value, profileVisibilitySchema),
                                    )
                                }
                                options={profileVisibilityValues.map((status) => ({
                                    label: capitalize(status),
                                    value: status,
                                }))}
                                className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
                                labelClassName="text-[10px]"
                            />

                            <SelectInput
                                label="Dataset Role"
                                value={filters.visibility}
                                onChange={(e) =>
                                    updateFilter(
                                        "role",
                                        validateEnum(e.target.value, profileDatasetRoleSchema),
                                    )
                                }
                                options={profileDatasetRoleValues.map((status) => ({
                                    label: capitalize(status),
                                    value: status,
                                }))}
                                className="py-1.5 px-2 text-xs bg-white/5 border-white/5 focus:border-primary-500/50"
                                labelClassName="text-[10px]"
                            />

                            <ToggleInput
                                label="Authored by me"
                                checked={filters.only_me}
                                onChange={(e) => updateFilter("only_me", e.target.checked)}
                                labelClassName="text-[10px]"
                            />
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
