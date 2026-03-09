import type React from "react";
import { forwardRef, useState } from "react";
import type { FieldError } from "react-hook-form";
import { VscEye, VscEyeClosed } from "react-icons/vsc";
import { cn } from "~/utils/classname.util";

export type TextInputProps = {
    label: string;
    className?: string;
    required?: boolean;
    error?: FieldError;
    redirect?: string;
    redirectHref?: string;
} & React.InputHTMLAttributes<HTMLInputElement>;

export const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
    (
        { label, className, required, error, redirect, redirectHref, ...props },
        ref,
    ) => {
        const [showPassword, setShowPassword] = useState(false);
        const isPassword = props.type === "password";
        const inputType = isPassword
            ? showPassword
                ? "text"
                : "password"
            : props.type;

        const togglePassword = () => setShowPassword((prev) => !prev);

        return (
            <div className="w-full space-y-2">
                <label>
                    <div className="flex justify-between items-center">
                        <div>
                            <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
                                {label}
                            </span>
                            {required && <span className="text-red-500 ml-1">*</span>}
                        </div>

                        {redirect && redirectHref && (
                            <a
                                href={redirectHref}
                                className="text-xs text-violet-400 hover:text-violet-300 hover:underline transition-colors"
                            >
                                {redirect}
                            </a>
                        )}
                    </div>

                    <div className="relative group">
                        <input
                            {...props}
                            ref={ref}
                            type={inputType}
                            className={cn(
                                "w-full bg-background border rounded-lg px-4 py-3 outline-none transition-all",
                                "placeholder:text-gray-600 text-white",
                                isPassword ? "pr-12" : "",
                                error
                                    ? "border-red-500 focus:ring-1 focus:ring-red-500"
                                    : "border-border focus:ring-2 focus:ring-violet-500",
                                className,
                            )}
                            aria-invalid={error ? "true" : "false"}
                        />

                        {isPassword && (
                            <button
                                type="button"
                                onClick={togglePassword}
                                className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 text-gray-500 hover:text-primary-400 transition-colors cursor-pointer"
                                tabIndex={-1}
                            >
                                {showPassword ? (
                                    <VscEyeClosed size={20} />
                                ) : (
                                    <VscEye size={20} />
                                )}
                            </button>
                        )}
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

TextInput.displayName = "TextInput";
