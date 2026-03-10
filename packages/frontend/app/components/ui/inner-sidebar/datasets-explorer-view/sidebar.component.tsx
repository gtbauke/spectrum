import { Footer } from "./footer.component";
import { Header } from "./header.component";
import { Results } from "./results.component";

export function DatasetExplorer() {
    return (
        <div className="flex flex-col h-full bg-[#111319]">
            <Header />
            <Results />
            <Footer />
        </div>
    );
}
