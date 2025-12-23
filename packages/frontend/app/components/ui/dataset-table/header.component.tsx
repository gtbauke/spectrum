export type DatasetTableHeaderProps = React.PropsWithChildren;

export function DatasetTableHeader({ children }: DatasetTableHeaderProps) {
    return <th className="w-fit p-2 bg-gray-800">{children}</th>;
}
