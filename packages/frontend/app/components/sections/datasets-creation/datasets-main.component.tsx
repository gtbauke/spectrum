import {
    flexRender,
    getCoreRowModel,
    getPaginationRowModel,
    useReactTable,
} from "@tanstack/react-table";
import { MainContainer } from "~/components/layout/main.component";
import { DatasetTableCell } from "~/components/ui/dataset-table/cell.component";
import { DatasetTableHeader } from "~/components/ui/dataset-table/header.component";
import { type DatasetFile, getColumnDefinitions } from "~/models/dataset.model";

export type DatasetsMainSectionProps = {
    file: DatasetFile | null;
};

export function DatasetsMainSection({ file }: DatasetsMainSectionProps) {
    const table = useReactTable({
        data: file?.rows || [],
        columns: getColumnDefinitions(file),
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        initialState: {
            pagination: {
                pageSize: 15,
            },
        },
    });

    if (file === null) {
        return (
            <MainContainer>
                <div className="text-center">
                    <h1 className="text-4xl font-bold">No datasets found!</h1>
                    <p className="text-gray-300">
                        Please, go back to the main page and upload a dataset
                    </p>
                </div>
            </MainContainer>
        );
    }

    return (
        <div className="text-center">
            <table style={{ width: table.getTotalSize() }}>
                <thead>
                    {table.getHeaderGroups().map((headerGroup) => (
                        <tr key={headerGroup.id}>
                            {headerGroup.headers.map((header) => (
                                <DatasetTableHeader key={header.id}>
                                    {flexRender(
                                        header.column.columnDef.header,
                                        header.getContext(),
                                    )}
                                </DatasetTableHeader>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody>
                    {table.getRowModel().rows.map((row, index) => (
                        <tr key={row.id}>
                            {row.getVisibleCells().map((cell) => (
                                <DatasetTableCell
                                    key={cell.id}
                                    invertBgColor={index % 2 === 0}
                                >
                                    {flexRender(
                                        cell.column.columnDef.cell,
                                        cell.getContext(),
                                    )}
                                </DatasetTableCell>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
