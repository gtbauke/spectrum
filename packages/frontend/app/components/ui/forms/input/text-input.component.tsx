import type React from "react";
import { forwardRef } from "react";
import { cn } from "~/utils/classname.util";
import { useFieldContext } from "../field/field-context";

export type TextInputProps = React.InputHTMLAttributes<HTMLInputElement>;

export const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
	({ className, id, ...props }, ref) => {
		const context = useFieldContext();
		const inputId = id || context.id;

		return (
			<input
				ref={ref}
				id={inputId}
				className={cn(
					"flex-1 bg-transparent border-none outline-none p-2 min-w-0 text-white placeholder:text-gray-600 appearance-none",
					className,
				)}
				aria-invalid={context.error ? "true" : "false"}
				disabled={context.disabled || props.disabled}
				{...props}
			/>
		);
	},
);

TextInput.displayName = "TextInput";
