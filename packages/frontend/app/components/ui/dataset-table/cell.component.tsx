import { cn } from "~/utils/classname.util";

export type DatasetTableCellProps = React.PropsWithChildren<{
    invertBgColor?: boolean;
}>;

export function DatasetTableCell({
    children,
    invertBgColor,
}: DatasetTableCellProps) {
    return (
        <td
            className={cn("p-2", {
                "bg-gray-600": invertBgColor,
            })}
        >
            {children}
        </td>
    );
}
