import { useState } from "react";
import { useDebounce } from "~/hooks/use-debounce.hook";
import { Footer } from "./footer.component";
import { Header } from "./header.component";
import { Results } from "./results.component";

export function DatasetExplorer() {
	const [search, setSearch] = useState("");
	const debouncedSearch = useDebounce(search, 300);

	return (
		<div className="flex flex-col h-full bg-[#111319]">
			<Header search={search} onSearchChange={setSearch} />
			<Results filters={{ name: debouncedSearch }} />
			<Footer />
		</div>
	);
}
