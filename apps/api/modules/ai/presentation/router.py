from fastapi import APIRouter

router = APIRouter()


@router.post("/predict")
async def predict() -> None:
    pass


@router.post("/predict/batch")
async def predict_batch() -> None:
    pass


@router.get("/predictions")
async def list_predictions() -> None:
    pass


@router.get("/predictions/{prediction_id}/explain")
async def explain_prediction(prediction_id: str) -> None:
    pass


@router.get("/models")
async def list_models() -> None:
    pass


@router.post("/models/retrain")
async def trigger_retrain() -> None:
    pass


@router.post("/feedback")
async def submit_feedback() -> None:
    pass
