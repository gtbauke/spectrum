import logging

from uuid import UUID
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.services import get_inference_service
from app.api.deps import UnitOfWork, get_uow
# from app.domain.inference.messages.base import BaseInferenceMessage
from app.domain.inference.query.tokenizer.tokenizer import QueryTokenizer
from app.domain.inference.query.parser.parser import InferenceQueryParser


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

            tokenizer = QueryTokenizer(raw["query"])
            tokens = tokenizer.tokenize()

            parser = InferenceQueryParser(tokens)
            ast = parser.parse_expression()
            logger.info("Parsed AST", extra={
                "model_id": model_id,
                "raw_message": raw,
                "ast": ast,
                "ast_json": ast.to_string(indent=0),
            })

            # message = BaseInferenceMessage.model_validate(raw)

            # result = await session.handle(message, raw_message=raw)
            # logger.info("Inference result", extra={
            #     "model_id": model_id,
            #     "raw_message": raw,
            #     "original_message": message.model_dump(),
            #     "result": result.model_dump(),
            # })

            # await websocket.send_json(result.model_dump())
            await websocket.send_json({
                "ast": ast.to_string(indent=0),
            })

    except WebSocketDisconnect:
        await websocket.close()
