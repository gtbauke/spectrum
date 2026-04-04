import type React from "react";
import { forwardRef } from "react";
import { cn } from "~/utils/classname.util";
import { useFieldContext } from "../field/field-context";

export type TextAreaInputProps =
	React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export const TextAreaInput = forwardRef<
	HTMLTextAreaElement,
	TextAreaInputProps
>(({ className, id, rows = 4, ...props }, ref) => {
	const context = useFieldContext();
	const inputId = id || context.id;

	return (
		<textarea
			ref={ref}
			id={inputId}
			rows={rows}
			className={cn(
				"flex-1 bg-transparent border-none outline-none p-2 min-w-0 text-white placeholder:text-gray-600 resize-y min-h-20",
				className,
			)}
			aria-invalid={context.error ? "true" : "false"}
			disabled={context.disabled || props.disabled}
			{...props}
		/>
	);
});

TextAreaInput.displayName = "TextAreaInput";
