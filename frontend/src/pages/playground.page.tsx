import { useEffect, useState } from "react";
import { useParams } from "react-router";
import useWebSocket, { ReadyState } from "react-use-websocket";

const WS_URL =
    "ws://127.0.0.1:8000/job/0684eb49-6d0e-4ed0-ac77-c107f0217e25/runs/b39c3854-5c01-455f-8a12-f32cce43495d/ws";

type PlaygroundPageParams = {
    datasetId: string;
};

export function PlaygroundPage() {
    const [query, setQuery] = useState("");

    const { datasetId } = useParams<PlaygroundPageParams>();
    const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(
        WS_URL,
        {
            share: false,
            shouldReconnect: () => true,
        },
    );

    useEffect(() => {
        console.log("Connection state changed!");
        if (readyState === ReadyState.OPEN) {
            sendJsonMessage({
                event: "subscribe",
                data: {
                    channel: "general-chatroom",
                },
            });
        }
    }, [readyState, sendJsonMessage]);

    useEffect(() => {
        console.log(`Got a new message: ${lastJsonMessage}`);
    }, [lastJsonMessage]);

    return (
        <div>
            <h1>Playground</h1>
            <p>Dataset: {datasetId}</p>

            <div>
                <label className="flex flex-col gap-2">
                    Query
                    <input
                        className="border border-white p-2"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <pre>{lastJsonMessage}</pre>
                </label>
            </div>
        </div>
    );
}
