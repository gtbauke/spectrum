import { useEffect } from "react";
import type { ProfileFilters } from "~/api/profiles.api";
import { useIntersection } from "~/hooks/use-intersection.hook";
import { useInfiniteProfiles } from "~/hooks/use-profiles.hook";
import { ProfileItem } from "./profile-item.component";

type ResultsProps = {
    filters: ProfileFilters;
};

export function Results({ filters }: ResultsProps) {
    const { data, isLoading, isFetchingNextPage, hasNextPage, fetchNextPage } =
        useInfiniteProfiles(filters);
    const { ref, isIntersecting } = useIntersection<HTMLDivElement>();

    useEffect(() => {
        if (isIntersecting && hasNextPage && !isFetchingNextPage) {
            fetchNextPage();
        }
    }, [isIntersecting, fetchNextPage, hasNextPage, isFetchingNextPage]);

    if (isLoading) {
        return (
            <div className="p-4 text-xs text-gray-500 animate-pulse">
                Loading workspaces...
            </div>
        );
    }

    const profiles = data?.pages.flatMap((page) => page.items) || [];

    if (!profiles.length) {
        return (
            <div className="p-4 text-xs text-gray-600 text-center mt-4">
                No profiles found.
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
                {profiles.map((profile) => (
                    <ProfileItem key={profile.id} profile={profile} />
                ))}
            </div>

            <div ref={ref} className="h-4 w-full shrink-0" aria-hidden="true" />

            {isFetchingNextPage && (
                <div className="py-2 text-center text-[10px] text-gray-500 font-medium uppercase tracking-wider animate-pulse">
                    Loading more...
                </div>
            )}

            {!hasNextPage && profiles.length > 0 && (
                <div className="py-4 text-center text-[10px] text-gray-600 font-medium">
                    End of results
                </div>
            )}
        </div>
    );
}
