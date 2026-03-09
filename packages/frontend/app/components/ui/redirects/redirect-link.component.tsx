import type { PropsWithChildren } from "react";
import { Link } from "react-router";
import { cn } from "~/utils/classname.util";

type RedirectLinkProps = PropsWithChildren<{
    to: string;
    className?: string;
}>;

export function RedirectLink({ children, to, className }: RedirectLinkProps) {
    return (
        <Link to={to} className={cn("text-primary-400 hover:underline", className)}>
            {children}
        </Link>
    )
}
