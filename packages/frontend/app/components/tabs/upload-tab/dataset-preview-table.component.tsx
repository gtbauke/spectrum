import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
} from "@tanstack/react-table";
import { useMemo } from "react";

type DatasetPreviewTableProps = {
	data: any[];
	columns: string[];
};

// TODO: type safe data
export function DatasetPreviewTable({
	data,
	columns,
}: DatasetPreviewTableProps) {
	const columnHelper = createColumnHelper<any>();

	const tableColumns = useMemo(() => {
		return columns.map((colName) =>
			columnHelper.accessor(colName, {
				header: colName,
				cell: (info) => {
					const val = info.getValue();

					if (val === null || val === undefined) {
						return <span className="text-gray-600">null</span>;
					}

					if (typeof val === "boolean") {
						return val ? "true" : "false";
					}

					return String(val);
				},
			}),
		);
	}, [columns, columnHelper]);

	const table = useReactTable({
		data,
		columns: tableColumns,
		getCoreRowModel: getCoreRowModel(),
	});

	return (
		<div className="h-full rounded-md border border-white/10 bg-[#1e2028] flex flex-col min-h-0">
			<div className="flex-1 overflow-auto custom-scrollbar">
				<table className="w-full text-sm text-left font-mono">
					<thead className="text-xs text-gray-400 uppercase sticky top-0 z-10 bg-[#1a1c23] shadow-md">
						{table.getHeaderGroups().map((headerGroup) => (
							<tr key={headerGroup.id}>
								{headerGroup.headers.map((header) => (
									<th
										key={header.id}
										className="px-4 py-3 font-medium whitespace-nowrap border-b border-white/5 border-r border-r-white/5 last:border-r-0"
									>
										{header.isPlaceholder
											? null
											: flexRender(
													header.column.columnDef.header,
													header.getContext(),
												)}
									</th>
								))}
							</tr>
						))}
					</thead>
					<tbody className="divide-y divide-white/5">
						{table.getRowModel().rows.map((row) => (
							<tr key={row.id} className="hover:bg-white/5 transition-colors">
								{row.getVisibleCells().map((cell) => (
									<td
										key={cell.id}
										className="px-4 py-2.5 whitespace-nowrap border-r border-r-white/5 last:border-r-0 text-gray-300"
									>
										{flexRender(cell.column.columnDef.cell, cell.getContext())}
									</td>
								))}
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	);
}
