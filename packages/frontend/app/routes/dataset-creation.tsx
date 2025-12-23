import { useDatasetCreationContext } from "~/contexts/dataset-creation.context";
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
    console.log(file);

    return (
        <MainContainer>
            <div className="text-center">
                <h1 className="text-4xl font-bold">Create a Dataset</h1>
            </div>
        </MainContainer>
    );
}
