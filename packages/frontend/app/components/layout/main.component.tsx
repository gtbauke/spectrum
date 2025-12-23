export function MainContainer({ children }: React.PropsWithChildren) {
    return (
        <main className="container mx-auto pt-16 p-4 w-full">{children}</main>
    );
}
