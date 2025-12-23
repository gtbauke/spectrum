import { MainContainer } from "~/components/layout/main.component";
import type { DatasetFile } from "~/models/dataset.model";

export type DatasetsMainSectionProps = {
    file: DatasetFile | null;
};

export function DatasetsMainSection({ file }: DatasetsMainSectionProps) {
    if (file === null) {
        return (
            <MainContainer>
                <div className="text-center">
                    <h1 className="text-4xl font-bold">No datasets found!</h1>
                    <p className="text-gray-300">
                        Please, go back to the main page and upload a dataset
                    </p>
                </div>
            </MainContainer>
        );
    }

    return (
        <MainContainer>
            <div className="text-center">
                <h1 className="text-4xl font-bold">Table goes here!</h1>
            </div>
        </MainContainer>
    );
}
