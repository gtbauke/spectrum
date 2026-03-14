// src/components/ui/toggle-input.component.tsx
import { forwardRef } from "react";
import type { FieldError } from "react-hook-form";
import { cn } from "~/utils/classname.util";

export type ToggleInputProps = {
    label: string;
    description?: string;
    className?: string;
    error?: FieldError;
    labelClassName?: string;
} & Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'>;

export const ToggleInput = forwardRef<HTMLInputElement, ToggleInputProps>(
    ({ label, description, className, error, labelClassName, ...props }, ref) => {
        return (
            <label className={cn("flex items-center gap-3 cursor-pointer group select-none", className)}>
                <div className="flex flex-col">
                    <span className={cn("text-xs font-medium text-gray-400 group-hover:text-gray-200 uppercase tracking-wider transition-colors", labelClassName)}>
                        {label}
                    </span>

                    {description && (
                        <span className="text-[10px] text-gray-500 leading-tight mt-0.5 group-hover:text-gray-400 transition-colors">
                            {description}
                        </span>
                    )}

                    {error?.message && (
                        <p className="text-xs text-red-500 mt-1 animate-in fade-in slide-in-from-top-1">
                            {error.message}
                        </p>
                    )}
                </div>

                <div className="relative flex items-center justify-center shrink-0 mt-0.5">
                    <input
                        {...props}
                        ref={ref}
                        type="checkbox"
                        className="peer sr-only"
                        aria-invalid={error ? "true" : "false"}
                    />

                    <div className={cn(
                        "w-8 h-4 rounded-full transition-colors duration-200 ease-in-out",
                        "bg-white/10 peer-checked:bg-primary-500/50",
                        "peer-focus-visible:ring-2 peer-focus-visible:ring-primary-500 peer-focus-visible:ring-offset-2 peer-focus-visible:ring-offset-background",
                        error && "ring-1 ring-red-500 bg-red-500/20"
                    )} />

                    <div className={cn(
                        "absolute left-0.5 w-3 h-3 rounded-full transition-transform duration-200 ease-in-out",
                        "bg-gray-400 peer-checked:translate-x-4 peer-checked:bg-primary-400",
                        "shadow-[0_1px_2px_rgba(0,0,0,0.4)]"
                    )} />
                </div>
            </label>
        );
    }
);

ToggleInput.displayName = "ToggleInput";
