import { forwardRef } from "react";
import type { FieldError } from "react-hook-form";
import { cn } from "~/utils/classname.util";

export type TextAreaInputProps = {
	label: string;
	className?: string;
	required?: boolean;
	error?: FieldError;
	labelClassName?: string;
} & React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export const TextAreaInput = forwardRef<
	HTMLTextAreaElement,
	TextAreaInputProps
>(
	(
		{ label, className, required, error, rows = 4, labelClassName, ...props },
		ref,
	) => {
		return (
			<div className="w-full space-y-2">
				<label>
					<div className="flex justify-between items-center">
						<div>
							<span
								className={cn(
									"text-xs font-medium text-gray-400 uppercase tracking-wider",
									labelClassName,
								)}
							>
								{label}
							</span>
							{required && <span className="text-red-500 ml-1">*</span>}
						</div>
					</div>

					<div className="relative group">
						<textarea
							{...props}
							ref={ref}
							rows={rows}
							className={cn(
								"w-full bg-background border rounded-lg px-4 py-3 outline-none transition-all",
								"placeholder:text-gray-600 text-white",
								"resize-y min-h-20",
								error
									? "border-red-500 focus:ring-1 focus:ring-red-500"
									: "border-border focus:ring-2 focus:ring-primary-500 hover:border-white/10",
								className,
							)}
							aria-invalid={error ? "true" : "false"}
						/>
					</div>

					{error?.message && (
						<p className="text-xs text-red-500 mt-1 animate-in fade-in slide-in-from-top-1">
							{error.message}
						</p>
					)}
				</label>
			</div>
		);
	},
);

TextAreaInput.displayName = "TextAreaInput";
