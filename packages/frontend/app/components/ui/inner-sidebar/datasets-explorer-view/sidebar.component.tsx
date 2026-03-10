import { useState } from "react";
import { Footer } from "./footer.component";
import { Header } from "./header.component";
import { Results } from "./results.component";

// TODO: add debounce

export function DatasetExplorer() {
    const [search, setSearch] = useState("");

    return (
        <div className="flex flex-col h-full bg-[#111319]">
            <Header />
            <Results />
            <Footer />
        </div>
    );
}
