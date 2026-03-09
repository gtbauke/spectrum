import type { PropsWithChildren } from "react";
import { cn } from "~/utils/classname.util";

export type ButtonProps = PropsWithChildren<{
    className?: string;
    type: "button" | "submit" | "reset";
}> & React.InputHTMLAttributes<HTMLButtonElement>;

export function Button({ className, children, type, ...props }: ButtonProps) {
    return (
        <button
            {...props}
            type={type}
            className={cn("w-full bg-primary-600 hover:bg-primary-700 text-white font-bold py-3 rounded-lg transition-all cursor-pointer", className)}
        >
            {children}
        </button>
    )
}
