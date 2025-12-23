import type { FieldError } from "react-hook-form";
import { cn } from "~/utils/classname.util";

export type FormTextAreaProps = {
    label: string;
    className?: string;
    required?: boolean;
    error?: FieldError;
} & React.DetailedHTMLProps<
    React.TextareaHTMLAttributes<HTMLTextAreaElement>,
    HTMLTextAreaElement
>;

export function FormTextArea({
    label,
    className,
    required,
    error,
    ...props
}: FormTextAreaProps) {
    return (
        <label className="flex flex-col gap-1">
            <span>
                {label}
                {required ? <span className="text-red-500"> *</span> : ""}
            </span>
            <textarea
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
