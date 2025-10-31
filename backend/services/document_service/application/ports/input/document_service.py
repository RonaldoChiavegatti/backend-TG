from abc import ABC, abstractmethod
from typing import IO, List
import uuid

from shared.models.base_models import DocumentJob as DocumentJobResponse


class DocumentService(ABC):
    """Input port defining the document service use cases."""

    @abstractmethod
    def start_document_processing(
        self, user_id: uuid.UUID, file_name: str, file_content: IO[bytes]
    ) -> DocumentJobResponse:
        """
        Use case for uploading a document and starting the processing workflow.
        """
        pass

    @abstractmethod
    def get_job_status(
        self, job_id: uuid.UUID, user_id: uuid.UUID
    ) -> DocumentJobResponse:
        """
        Use case for checking the status of a specific processing job.
        """
        pass

    @abstractmethod
    def get_user_jobs(self, user_id: uuid.UUID) -> List[DocumentJobResponse]:
        """
        Use case for retrieving all jobs for a specific user.
        """
        pass
