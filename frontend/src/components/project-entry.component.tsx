import { clsx } from "clsx";
import type { PropsWithChildren } from "react";
import { IoPencil } from "react-icons/io5";
import { useLocation } from "react-router";

type ProjectEntryProps = PropsWithChildren<{
    datasetId: string;
}>;

export function ProjectEntry({ children, datasetId }: ProjectEntryProps) {
    const { pathname } = useLocation();
    const isSamePathname = pathname === `/datasets/${datasetId}`;

    return (
        <div
            className={clsx(
                "flex content-center items-center gap-2 text-gray-300 transition-colors duration-100 ease-in-out hover:text-white",
                {
                    "text-white": isSamePathname,
                },
            )}
        >
            <IoPencil />
            <a href={`/datasets/${datasetId}`}>{children}</a>
        </div>
    );
}
