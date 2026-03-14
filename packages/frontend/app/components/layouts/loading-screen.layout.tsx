export function LoadingScreen() {
    return (
        <div className="fixed inset-0 bg-[#111319] flex flex-col items-center justify-center z-9999">
            <div className="w-12 h-12 border-2 border-primary-500/20 border-t-primary-500 rounded-full animate-spin" />
            <span className="mt-4 text-[10px] uppercase tracking-[0.2em] text-gray-500 font-medium">
                Initializing Spectrum
            </span>
        </div>
    );
}
