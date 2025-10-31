import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from shared.models.base_models import DocumentJob as DocumentJobResponse
from services.document_service.application.ports.input.document_service import (
    DocumentService,
)
from services.document_service.application.exceptions import (
    JobNotFoundError,
    JobAccessForbiddenError,
)
from services.document_service.infrastructure.dependencies import get_document_service
from services.document_service.infrastructure.security import get_current_user_id

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/upload", response_model=DocumentJobResponse, status_code=status.HTTP_202_ACCEPTED
)
def upload_document(
    file: UploadFile = File(...),
    user_id: uuid.UUID = Depends(get_current_user_id),
    doc_service: DocumentService = Depends(get_document_service),
):
    try:
        job = doc_service.start_document_processing(
            user_id=user_id, file_name=file.filename, file_content=file.file
        )
        return job
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start processing: {e}",
        )


@router.get("/jobs/{job_id}", response_model=DocumentJobResponse)
def get_job_status_endpoint(
    job_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    doc_service: DocumentService = Depends(get_document_service),
):
    try:
        job = doc_service.get_job_status(job_id=job_id, user_id=user_id)
        return job
    except JobNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except JobAccessForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/jobs", response_model=List[DocumentJobResponse])
def get_user_jobs_endpoint(
    user_id: uuid.UUID = Depends(get_current_user_id),
    doc_service: DocumentService = Depends(get_document_service),
):
    try:
        jobs = doc_service.get_user_jobs(user_id=user_id)
        return jobs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
