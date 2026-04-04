import type { Monaco } from "@monaco-editor/react";
import type { Model } from "~/schemas/domain/model.schema";

let registered = false;
let currentModels: Model[] = [];

/**
 * Updates the global model list used for autocompletion.
 */
export function updateAutocompleteModels(models: Model[]) {
	currentModels = models;
}

/**
 * Registers a global completion provider for the 'sql' language in Monaco.
 * This should be called once (e.g. in the first block that mounts).
 */
export function setupMonacoAutocomplete(monaco: Monaco) {
	if (registered) return;

	monaco.languages.registerCompletionItemProvider("sql", {
		triggerCharacters: [" "],
		provideCompletionItems: (model: any, position: any) => {
			const lineContent = model.getLineContent(position.lineNumber);
			const textUntilPosition = lineContent.substring(0, position.column - 1);

			// Check if we are after a 'FROM' token (case-insensitive)
			if (!/\bFROM\s+$/i.test(textUntilPosition)) {
				return { suggestions: [] };
			}

			const suggestions = currentModels.map((m) => ({
				label: m.name,
				kind: monaco.languages.CompletionItemKind.File,
				insertText: m.name,
				detail: `Model from Job Run`,
				range: {
					startLineNumber: position.lineNumber,
					endLineNumber: position.lineNumber,
					startColumn: position.column,
					endColumn: position.column,
				} as any,
			}));

			return { suggestions };
		},
	});

	registered = true;
}
