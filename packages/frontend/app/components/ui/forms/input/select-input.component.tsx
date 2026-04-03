import { ChevronDown } from "lucide-react";
import { forwardRef } from "react";
import type { FieldError } from "react-hook-form";
import { cn } from "~/utils/classname.util";

export type SelectOption = {
	value: string;
	label: string;
};

export type SelectInputProps = {
	label: string;
	className?: string;
	required?: boolean;
	error?: FieldError | string;
	options: SelectOption[];
	labelClassName?: string;
} & Omit<React.SelectHTMLAttributes<HTMLSelectElement>, "children">;

export const SelectInput = forwardRef<HTMLSelectElement, SelectInputProps>(
	(
		{ label, className, required, error, options, labelClassName, ...props },
		ref,
	) => {
		const hasError = Boolean(error);
		const errorMessage = typeof error === "string" ? error : error?.message;

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

					<div className="relative group mt-2">
						<select
							{...props}
							ref={ref}
							className={cn(
								"w-full bg-background border rounded-lg px-4 py-3 outline-none transition-all appearance-none cursor-pointer",
								"text-white placeholder:text-gray-600",
								error
									? "border-red-500 focus:ring-1 focus:ring-red-500"
									: "border-border focus:ring-2 focus:ring-violet-500 hover:border-white/10",
								className,
							)}
							aria-invalid={error ? "true" : "false"}
						>
							{options.map((option) => (
								<option
									key={option.value}
									value={option.value}
									className="bg-[#111319]"
								>
									{option.label}
								</option>
							))}
						</select>

						<div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500 group-hover:text-gray-300 transition-colors">
							<ChevronDown size={16} />
						</div>
					</div>

					{hasError && (
						<p className="text-xs text-red-500 mt-1 animate-in fade-in slide-in-from-top-1">
							{errorMessage}
						</p>
					)}
				</label>
			</div>
		);
	},
);

SelectInput.displayName = "SelectInput";
