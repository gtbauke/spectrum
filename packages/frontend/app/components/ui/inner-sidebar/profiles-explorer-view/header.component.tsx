import { useState } from "react";
import type { ProfileFilters } from "~/api/profiles.api";
import { cn } from "~/utils/classname.util";
import { SidebarSearchInput } from "../searchbar.component";
import { SidebarTitle } from "../title.component";
import { ProfilesAdvancedFilters } from "./advanced-filters.component";

type HeaderProps = {
    className?: string;
    filters: ProfileFilters;
    onFiltersChange: (filters: ProfileFilters) => void;
};

export function Header({ className, filters, onFiltersChange }: HeaderProps) {
    const [isAdvancedFilterOpen, setIsAdvancedFilterOpen] = useState(false);

    const activeFilterCount = Object.entries(filters).filter(
        ([, val]) => val !== "" && val !== false,
    ).length;

    const updateFilter = <TKey extends keyof ProfileFilters>(
        key: TKey,
        value: ProfileFilters[TKey],
    ) => {
        onFiltersChange({ ...filters, [key]: value });
    };

    const clearFilters = () => {
        onFiltersChange({});
    };

    return (
        <div
            className={cn(
                "flex flex-col border-b border-white/5 shrink-0",
                className,
            )}
        >
            <div className="p-4 pb-3 space-y-3">
                <SidebarTitle
                    toggleFilter={() => setIsAdvancedFilterOpen((prev) => !prev)}
                    activeFilterCount={activeFilterCount}
                >
                    Profiles Search
                </SidebarTitle>

                <SidebarSearchInput
                    type="text"
                    search={filters.name || ""}
                    onSearchChange={(value) => updateFilter("name", value)}
                    placeholder="Search by name..."
                />
            </div>

            <ProfilesAdvancedFilters
                isAdvancedFilterOpen={isAdvancedFilterOpen}
                activeFilterCount={activeFilterCount}
                filters={filters}
                updateFilter={updateFilter}
                clearFilters={clearFilters}
            />
        </div>
    );
}
