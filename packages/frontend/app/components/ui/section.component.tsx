import type { PropsWithChildren } from "react";

type SectionProps = PropsWithChildren<{
	title: string;
}>;

export function Section({ children, title }: SectionProps) {
	return (
		<section className="border p-4 rounded shadow space-y-4 border-gray-800">
			<h2 className="text-xl font-bold">{title}</h2>
			{children}
		</section>
	);
}
