import Editor, { loader } from "@monaco-editor/react";
import { type InferenceData, useEditorStore } from "~/stores/editor.store";

loader.config({
    paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs" },
});

export function InferenceBlock({
    id,
    data,
}: {
    id: string;
    data: InferenceData;
}) {
    const updateBlock = useEditorStore((state) => state.updateBlock);

    const handleEditorChange = (value: string | undefined) => {
        updateBlock(id, { code: value || "" });
    };

    return (
        <div className="space-y-2">
            <div className="flex items-center justify-between px-1">
                <span className="text-[10px] font-mono text-gray-500 uppercase tracking-widest">
                    IQL Inference Script
                </span>
            </div>

            <div className="rounded-md overflow-hidden border border-white/5 bg-[#0d0e12]">
                <Editor
                    height="200px"
                    language="sql"
                    theme="vs-dark"
                    value={data.code}
                    onChange={handleEditorChange}
                    options={{
                        minimap: { enabled: false },
                        fontSize: 12,
                        lineNumbers: "on",
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                        padding: { top: 10, bottom: 10 },
                        fontFamily: "'Fira Code', 'Cascadia Code', monospace",
                    }}
                    onMount={(_, monaco) => {
                        monaco.editor.defineTheme("spectrum-dark", {
                            base: "vs-dark",
                            inherit: true,
                            rules: [],
                            colors: {
                                "editor.background": "#0d0e12",
                                "editor.lineHighlightBackground": "#ffffff05",
                            },
                        });
                        monaco.editor.setTheme("spectrum-dark");
                    }}
                />
            </div>
        </div>
    );
}
