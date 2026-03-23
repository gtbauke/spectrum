import { useState } from "react";
import type { ProfileFilter } from "~/schemas/dtos/profile.dto";
import { useDebounce } from "~/hooks/use-debounce.hook";
import { Header } from "./header.component";
import { Results } from "./results.component";

export function ProfilesExplorer() {
    const [filters, setFilters] = useState<ProfileFilter>({});

    const debouncedFilters = useDebounce(filters, 300);

    return (
        <div className="flex flex-col h-full bg-[#111319] border-r border-white/5 w-64 select-none">
            <Header filters={filters} onFiltersChange={setFilters} />
            <Results filters={debouncedFilters} />
        </div>
    );
}
