import { useRef } from "react";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { type MetadataData, useEditorStore } from "~/stores/editor.store";

export function MetadataBlock({
    id,
    data,
}: {
    id: string;
    data: MetadataData;
}) {
    const updateBlock = useEditorStore((state) => state.updateBlock);
    const commit = useEditorStore((state) => state.commit);

    const timerRef = useRef<NodeJS.Timeout | null>(null);

    const handleTextChange = (field: string, value: string) => {
        updateBlock(id, { [field]: value }, { recordHistory: false });

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
                value={data.name || ""}
                onChange={(e) => handleTextChange("name", e.target.value)}
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
                value={data.description || ""}
                onChange={(e) => handleTextChange("description", e.target.value)}
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
