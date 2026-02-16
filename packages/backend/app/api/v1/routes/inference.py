import logging

from uuid import UUID
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.services import get_inference_service
from app.api.deps import UnitOfWork, get_uow


inference_router = APIRouter(tags=["Inference"])
logger = logging.getLogger(__name__)


@inference_router.websocket("/{model_id}/ws")
async def websocket_inference(
    websocket: WebSocket,
    model_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
):
    await websocket.accept()
    inference_service = get_inference_service()

    async with uow:
        _session = await inference_service.create_inference_session(uow=uow, model_id=model_id)

    try:
        while True:
            raw = await websocket.receive_json()

            if "code" in raw:
                result = await _session.handle_unsafe_code_execution(raw["code"])
            elif "query" in raw:
                result = await _session.execute_query(raw["query"])
            else:
                await websocket.send_json({
                    "error": "Invalid message format. Expected 'code' or 'query' field.",
                })

                continue

            await websocket.send_json({
                "result": result,
            })

    except WebSocketDisconnect:
        await websocket.close()
