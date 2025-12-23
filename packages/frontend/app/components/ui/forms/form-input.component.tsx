import type { FieldError } from "react-hook-form";
import { cn } from "~/utils/classname.util";

export type FormInputProps = {
    label: string;
    className?: string;
    required?: boolean;
    error?: FieldError;
} & React.DetailedHTMLProps<
    React.InputHTMLAttributes<HTMLInputElement>,
    HTMLInputElement
>;

export function FormInput({
    label,
    className,
    required,
    error,
    ...props
}: FormInputProps) {
    return (
        <label className="flex flex-col gap-1">
            <span>
                {label}
                {required ? <span className="text-red-500"> *</span> : ""}
            </span>
            <input
                {...props}
                className={cn(className, "p-2 bg-gray-800 rounded-sm")}
                aria-invalid={error ? "true" : "false"}
            />
            {error && (
                <span className="text-sm text-red-500">{error.message}</span>
            )}
        </label>
    );
}
