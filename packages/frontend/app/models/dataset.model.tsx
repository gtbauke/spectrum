import type { ColumnDef } from "@tanstack/react-table";

export type DatasetFile = {
	header: string[];
	rows: Record<string, number>[];
	originalName: string;
	upload: File;
};

const formatter = new Intl.NumberFormat("en-US", {
	minimumFractionDigits: 2,
	maximumFractionDigits: 2,
});

export function getColumnDefinitions(
	file: DatasetFile | null,
): ColumnDef<Record<string, number>, number>[] {
	if (file === null) {
		return [];
	}

	return file.header.map((header) => ({
		accessorKey: header,
		header,
		cell: (props) => <p>{formatter.format(props.getValue())}</p>,
	}));
}
