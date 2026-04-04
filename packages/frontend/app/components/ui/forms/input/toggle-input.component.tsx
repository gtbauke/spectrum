import { forwardRef } from "react";
import { cn } from "~/utils/classname.util";
import { useFieldContext } from "../field/field-context";

export type ToggleInputProps = Omit<
	React.InputHTMLAttributes<HTMLInputElement>,
	"type"
> & { value?: boolean };

export const ToggleInput = forwardRef<HTMLInputElement, ToggleInputProps>(
	({ className, id, ...props }, ref) => {
		const context = useFieldContext();
		const inputId = id || context.id;

		return (
			<div className="relative flex items-center justify-center shrink-0">
				<input
					{...props}
					id={inputId}
					ref={ref}
					type="checkbox"
					className="peer sr-only"
					aria-invalid={context.error ? "true" : "false"}
					disabled={context.disabled || props.disabled}
				/>

				<div
					className={cn(
						"w-8 h-4 rounded-full transition-colors duration-200 ease-in-out cursor-pointer",
						"bg-white/10 peer-checked:bg-primary-500/50",
						"peer-focus-visible:ring-2 peer-focus-visible:ring-primary-500 peer-focus-visible:ring-offset-2 peer-focus-visible:ring-offset-background",
						context.error && "ring-1 ring-red-500 bg-red-500/20",
						className,
					)}
				/>

				<div
					className={cn(
						"absolute left-0.5 w-3 h-3 rounded-full transition-transform duration-200 ease-in-out pointer-events-none",
						"bg-gray-400 peer-checked:translate-x-4 peer-checked:bg-primary-400",
						"shadow-[0_1px_2px_rgba(0,0,0,0.4)]",
					)}
				/>
			</div>
		);
	},
);

ToggleInput.displayName = "ToggleInput";
