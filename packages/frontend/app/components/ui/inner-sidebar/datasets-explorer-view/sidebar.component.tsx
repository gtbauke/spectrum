import { useState } from "react";
import { Footer } from "./footer.component";
import { Header } from "./header.component";
import { Results } from "./results.component";

// TODO: add debounce

export function DatasetExplorer() {
    const [search, setSearch] = useState("");
    const [page, setPage] = useState(1);

    return (
        <div className="flex flex-col h-full bg-[#111319]">
            <Header search={search} onSearchChange={setSearch} />
            <Results search={search} page={page} onPageChange={setPage} />
            <Footer />
        </div>
    );
}
