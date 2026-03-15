import { useEffect } from "react";
import type { ProfileFilters } from "~/api/profiles.api";
import { useIntersection } from "~/hooks/use-intersection.hook";
import { useInfiniteProfiles } from "~/hooks/use-profiles.hook";
import { useEditorStore } from "~/stores/editor.store";
import { ProfileItem } from "./profile-item.component";

type ResultsProps = {
	filters: ProfileFilters;
};

export function Results({ filters }: ResultsProps) {
	const tabs = useEditorStore((state) => state.tabs);
	const tabIds = useEditorStore((state) => state.tabIds);
	const openTab = useEditorStore((state) => state.openTab);

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
	const draftTabs = tabIds
		.map((tab) => {
			const tabState = tabs[tab];
			if (tabState.type !== "profile") {
				return null;
			}

			return tabState;
		})
		.filter(
			(tabState) =>
				tabState && !profiles.some((p) => p.id === tabState.data.profileId),
		);

	const handleCreateDraft = () => {
		// TODO: create profile in the backend
		const tempId = crypto.randomUUID();

		openTab({
			id: tempId,
			type: "profile",
			data: {
				blocks: [],
				isDirty: true,
				future: [],
				past: [],
				activeBlockId: null,
				name: "Untitled Profile",
				description: null,
				profileId: tempId,
				versionId: crypto.randomUUID(),
			},
		});
	};

	if (!profiles.length) {
		return (
			<div className="p-4 text-xs text-gray-600 text-center mt-4">
				No profiles found.
			</div>
		);
	}

	return (
		<div className="flex-1 flex flex-col overflow-hidden">
			{draftTabs.length > 0 && (
				<div className="space-y-4 py-2">
					<div className="px-4 py-1 text-[10px] font-bold text-gray-500 uppercase">
						Unsaved Drafts
					</div>
					<div className="flex-1 overflow-y-auto px-2 space-y-1 custom-scrollbar">
						{draftTabs.map((tab) => {
							if (tab?.type !== "profile") {
								return null;
							}

							return (
								// <ProfileItem
								// 	key={tab.id}
								// 	profile={{
								// 		created_at: tab.profileVersion.timestamp,
								// 		updated_at: tab.profileVersion.timestamp,
								// 		id: tab.profileId,
								// 		owner_id: "", // TODO: get owner id
								// 		versions: [tab.profileVersion],
								// 	}}
								// />
								<p key={tab.id}>Draft Profiles are not supported yet.</p>
							);
						})}
					</div>
				</div>
			)}

			<div className="space-y-4 py-2">
				<div className="px-4 py-1 text-[10px] font-bold text-gray-500 uppercase">
					Saved Profiles
				</div>
				<div className="flex-1 overflow-y-auto px-2 space-y-1 custom-scrollbar">
					{profiles.map((profile) => (
						<ProfileItem key={profile.id} profile={profile} />
					))}
				</div>
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
