import type { ColumnDef } from "@tanstack/react-table";

export type DatasetFile = {
    header: string[];
    rows: Record<string, number>[];
};

export function getColumnDefinitions(
    file: DatasetFile,
): ColumnDef<Record<string, number>, unknown>[] {
    return file.header.map(
        (header) =>
            ({
                accessorKey: header,
                header,
                cell: (props) => <p>{props.getValue() as string}</p>,
            }) satisfies ColumnDef<Record<string, number>, unknown>,
    );
}
