import { LeftBarLayout } from "~/components/layout/left-bar.component";
import { DatasetsAsideSection } from "~/components/sections/datasets-creation/datasets-aside.component";
import { DatasetsMainSection } from "~/components/sections/datasets-creation/datasets-main.component";
import { useDatasetCreationContext } from "~/contexts/dataset-creation.context";
import type { Route } from "../+types/root";

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

    return (
        <LeftBarLayout
            Aside={DatasetsAsideSection}
            Main={DatasetsMainSection}
            mainProps={{
                file,
            }}
        />
    );
}
