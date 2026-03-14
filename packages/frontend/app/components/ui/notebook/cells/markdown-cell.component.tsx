import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { useEditorStore } from "~/stores/editor.store";
import { cn } from "~/utils/classname.util";

type MarkdownBlockProps = {
    id: string;
    data: { value: string };
    isActive: boolean;
};

export function MarkdownBlock({ id, data, isActive }: MarkdownBlockProps) {
    const updateBlock = useEditorStore((state) => state.updateBlock);
    const commit = useEditorStore((state) => state.commit);

    const [isEditing, setIsEditing] = useState(false);
    const timerRef = useRef<NodeJS.Timeout | null>(null);

    useEffect(() => {
        if (isActive && data.value === "") {
            setIsEditing(true);
        }
    }, [isActive, data.value]);

    const handleTextChange = (value: string) => {
        updateBlock(id, { value }, { recordHistory: false });

        if (timerRef.current) clearTimeout(timerRef.current);
        timerRef.current = setTimeout(() => {
            commit();
        }, 500);
    };

    const handleBlur = () => {
        setIsEditing(false);
        if (timerRef.current) {
            clearTimeout(timerRef.current);
            commit();
        }
    };

    return (
        // biome-ignore lint/a11y/noStaticElementInteractions: Cannot have nested interactive elements
        <div className="w-full min-h-10" onDoubleClick={() => setIsEditing(true)}>
            {isEditing ? (
                <TextAreaInput
                    label="Markdown Editor"
                    value={data.value}
                    autoFocus
                    onChange={(e) => handleTextChange(e.target.value)}
                    onBlur={handleBlur}
                    placeholder="Type markdown here..."
                    className="bg-transparent border-none p-0 focus:ring-0 font-mono text-sm leading-relaxed"
                />
            ) : (
                <div
                    className={cn(
                        "prose prose-invert prose-sm max-w-none cursor-text",
                        data.value === "" ? "italic text-gray-600" : "text-gray-300",
                    )}
                >
                    {data.value === "" ? (
                        "Double-click to edit markdown..."
                    ) : (
                        <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                        >
                            {data.value}
                        </ReactMarkdown>
                    )}
                </div>
            )}
        </div>
    );
}
