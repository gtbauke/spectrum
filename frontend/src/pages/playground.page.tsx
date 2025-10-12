import Editor, { type OnMount } from "@monaco-editor/react";
import type * as monacoType from "monaco-editor/esm/vs/editor/editor.api";
import { type FormEvent, useRef } from "react";
import { useParams } from "react-router";

type PlaygroundPageParams = {
    datasetId: string;
};

export function PlaygroundPage() {
    const { datasetId } = useParams<PlaygroundPageParams>();
    const editorRef = useRef<monacoType.editor.IStandaloneCodeEditor | null>(
        null,
    );

    const handleFormSubmit = (formEvent: FormEvent<HTMLFormElement>) => {
        formEvent.preventDefault();
        console.log(editorRef.current?.getValue());
    };

    const handleEditorOnMount: OnMount = (editor) => {
        editorRef.current = editor;
    };

    return (
        <div className="space-y-8 text-white">
            <div>
                <h1>Playground</h1>
                <p>Dataset: {datasetId}</p>
            </div>

            <form className="space-y-4" onSubmit={handleFormSubmit}>
                <Editor
                    onMount={handleEditorOnMount}
                    className="min-h-[400px]"
                    theme="vs-dark"
                    options={{
                        minimap: {
                            enabled: false,
                        },
                    }}
                    defaultLanguage="sql"
                    defaultValue="-- Write your query here"
                />

                <button
                    type="submit"
                    className="w-full cursor-pointer rounded bg-green-700 p-2 hover:bg-green-800 active:bg-green-900"
                >
                    Run
                </button>
            </form>
        </div>
    );
}
