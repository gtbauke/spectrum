import {
    flexRender,
    getCoreRowModel,
    useReactTable,
} from "@tanstack/react-table";
import { LeftBarLayout } from "~/components/layout/left-bar.component";
import { DatasetsAsideSection } from "~/components/sections/datasets-creation/datasets-aside.component";
import { DatasetsMainSection } from "~/components/sections/datasets-creation/datasets-main.component";
import { useDatasetCreationContext } from "~/contexts/dataset-creation.context";
import { getColumnDefinitions } from "~/models/dataset.model";
import type { Route } from "../+types/root";
import { MainContainer } from "../components/layout/main.component";

export function meta(_: Route.MetaArgs) {
    return [
        { title: "Spectrum" },
        {
            name: "description",
            content: "The web platform for Symbolic Regression",
        },
    ];
}

export default function DatasetCreation() {
    const { file } = useDatasetCreationContext();
    const table = useReactTable({
        data: file?.rows || [],
        columns: getColumnDefinitions(file),
        getCoreRowModel: getCoreRowModel(),
    });

    // TODO: remove if and return default left bar layout
    if (file === null) {
        return (
            <LeftBarLayout
                Aside={DatasetsAsideSection}
                Main={DatasetsMainSection}
                mainProps={{
                    file,
                }}
            />
        );
    }

    // TODO: move to table component and to DatasetsMainSection component
    return (
        <MainContainer>
            <div className="text-center">
                <h1 className="text-4xl font-bold">Create a Dataset</h1>

                <table style={{ width: table.getTotalSize() }}>
                    <thead>
                        {table.getHeaderGroups().map((headerGroup) => (
                            <tr key={headerGroup.id}>
                                {headerGroup.headers.map((header) => (
                                    <th
                                        key={header.id}
                                        style={{ width: header.getSize() }}
                                    >
                                        {
                                            header.column.columnDef
                                                .header as string
                                        }
                                    </th>
                                ))}
                            </tr>
                        ))}
                    </thead>
                    <tbody>
                        {table.getRowModel().rows.map((row) => (
                            <tr key={row.id}>
                                {row.getVisibleCells().map((cell) => (
                                    <td
                                        key={cell.id}
                                        style={{ width: cell.column.getSize() }}
                                    >
                                        {flexRender(
                                            cell.column.columnDef.cell,
                                            cell.getContext(),
                                        )}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </MainContainer>
    );
}
