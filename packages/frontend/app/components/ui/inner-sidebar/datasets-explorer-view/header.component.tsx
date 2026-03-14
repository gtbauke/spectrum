import { Filter } from "lucide-react";
import { useState } from "react";
import { SidebarSearchInput } from "../searchbar.component";
import { SidebarTitle } from "../title.component";

type HeaderProps = {
    search: string;
    onSearchChange: (value: string) => void;
};

export function Header({ search, onSearchChange }: HeaderProps) {
    const [isAdvancedFilterOpen, setIsAdvancedFilterOpen] = useState(false);

    return (
        <div className="p-4 space-y-3 border-b border-border shrink-0">
            <SidebarTitle
                toggleFilter={() => setIsAdvancedFilterOpen((prev) => !prev)}
            >
                Global Search
            </SidebarTitle>

            <SidebarSearchInput
                type="text"
                search={search}
                onSearchChange={onSearchChange}
                placeholder="Search by name..."
            />
        </div>
    );
}
