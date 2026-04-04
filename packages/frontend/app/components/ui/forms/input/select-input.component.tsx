import { ChevronDown } from "lucide-react";
import { forwardRef } from "react";
import { cn } from "~/utils/classname.util";
import { useFieldContext } from "../field/field-context";

export type SelectOption = {
	value: string;
	label: string;
};

export type SelectInputProps = {
	options: SelectOption[];
} & Omit<React.SelectHTMLAttributes<HTMLSelectElement>, "children">;

export const SelectInput = forwardRef<HTMLSelectElement, SelectInputProps>(
	({ className, id, options, ...props }, ref) => {
		const context = useFieldContext();
		const inputId = id || context.id;

		return (
			<div className={cn("relative flex-1 flex", className)}>
				<select
					ref={ref}
					id={inputId}
					className={cn(
						"flex-1 bg-transparent border-none outline-none p-2 min-w-0 appearance-none cursor-pointer text-white placeholder:text-gray-600",
					)}
					aria-invalid={context.error ? "true" : "false"}
					disabled={context.disabled || props.disabled}
					{...props}
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
				<div className="absolute right-0 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500 group-hover:text-gray-300 transition-colors">
					<ChevronDown size={16} />
				</div>
			</div>
		);
	},
);

SelectInput.displayName = "SelectInput";
