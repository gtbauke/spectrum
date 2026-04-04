import * as React from "react";
import type { FieldError } from "react-hook-form";

export type FieldContextValue = {
	id: string;
	error?: FieldError | string;
	required?: boolean;
	disabled?: boolean;
};

export const FieldContext = React.createContext<FieldContextValue | null>(null);

export function useFieldContext() {
	const context = React.useContext(FieldContext);
	if (!context) {
		throw new globalThis.Error("useFieldContext must be used within a Field.Root");
	}
	return context;
}
