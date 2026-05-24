from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.modules.document.service import DocumentService
from app.modules.document.dto import DocumentResponse
from app.modules.user.models import User
from app.rag.pipeline import pipeline

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DocumentService(db)
    print(f"Uploading document for user_id: {current_user}")
    document = await service.upload(file, current_user.id)
    background_tasks.add_task(
        pipeline.index_document,
        document.file_path,
        current_user.id,
        document.id,
    )
    return document