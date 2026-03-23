import { useRef } from "react";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { type EditorTab, useEditorStore } from "~/stores/editor.store";

export function MetadataBlock({
    id,
    tabId,
}: {
    id: string;
    tabId: string;
}) {
    const tab = useEditorStore((state) => state.tabs[tabId]);
    if (!tab || tab.type !== "profile") return null;

    const profile = tab.data.profile;
    const updateTab = useEditorStore((state) => state.updateTab);
    const commit = useEditorStore((state) => state.commit);

    const timerRef = useRef<NodeJS.Timeout | null>(null);

    const handleTextChange = (field: "name" | "description", value: string) => {
        if (!profile) return;

        updateTab(tabId, "profile", {
            profile: {
                ...profile,
                [field]: value,
            }
        });

        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }

        timerRef.current = setTimeout(() => {
            commit();
        }, 500);
    };

    return (
        <div className="space-y-4">
            <TextInput
                label="Profile Name"
                value={profile?.name || ""}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleTextChange("name", e.target.value)}
                className="bg-transparent border-none px-0 py-0 text-lg font-medium focus:ring-0"
                onBlur={() => {
                    if (timerRef.current) {
                        clearTimeout(timerRef.current);
                        commit();
                        timerRef.current = null;
                    }
                }}
            />
            <TextAreaInput
                label="Description"
                value={profile?.description || ""}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleTextChange("description", e.target.value)}
                className="bg-transparent border-none px-0 py-0 text-sm focus:ring-0 min-h-15"
                placeholder="Document the objective..."
                onBlur={() => {
                    if (timerRef.current) {
                        clearTimeout(timerRef.current);
                        commit();
                        timerRef.current = null;
                    }
                }}
            />
        </div>
    );
}
