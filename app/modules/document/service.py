import os
import shutil
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import config
from app.core.exceptions import DocumentException
from app.modules.document.models import Document


class DocumentService:
    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def upload(self, file: UploadFile, user_id: int) -> Document:
        # Step 1 - validate file type
        if not file.filename or not file.filename.endswith(".pdf"):
            raise DocumentException.INVALID_FILE_TYPE

        # Step 2 - save file to disk
        upload_dir = config.UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{uuid4()}_{file.filename}")
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Step 3 - save metadata to DB
        document = Document(
            user_id=user_id,
            file_name=file.filename,
            file_path=file_path,
            status="processing",
        )
        self.__db.add(document)
        await self.__db.flush()
        await self.__db.refresh(document)

        return document