import type { DatasetsMainSectionProps } from "../sections/datasets-creation/datasets-main.component";

export type LeftBatLayoutProps = {
    Aside: () => React.ReactNode;
    Main: (props: DatasetsMainSectionProps) => React.ReactNode;

    mainProps: DatasetsMainSectionProps;
};

export function LeftBarLayout({ Aside, Main, mainProps }: LeftBatLayoutProps) {
    return (
        <main className="flex h-screen">
            <aside className="min-w-72 shadow-lg">
                <Aside />
            </aside>
            <div className="flex-1">
                <Main {...mainProps} />
            </div>
        </main>
    );
}
