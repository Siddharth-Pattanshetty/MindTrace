import logging
from fastapi import APIRouter, HTTPException, Depends, status
from app.ai.error_classifier.service import ErrorClassifierService, get_error_classifier_service
from app.ai.error_classifier.schemas import ErrorClassificationRequest, ErrorClassificationResponse, ModelInfoResponse
from app.ai.concept_engine.service import ConceptEngineService, get_concept_engine_service
from app.ai.concept_engine.schemas import (
    ConceptClassificationRequest,
    ConceptClassificationResponse,
    AttemptAnalysisRequest,
    AttemptAnalysisResponse,
    ErrorDetail,
    ConceptDetail
)

logger = logging.getLogger("mindtrace.api.ai")

router = APIRouter()

@router.post("/classify-error", response_model=ErrorClassificationResponse, summary="Classify student error type")
def classify_error(
    request: ErrorClassificationRequest,
    error_service: ErrorClassifierService = Depends(get_error_classifier_service)
):
    """
    Classifies a student's answer error type using TF-IDF + Logistic Regression trained model.
    Accepts question, student_answer, work_evidence, and optional correct_answer.
    """
    try:
        return error_service.classify_error(request)
    except Exception as e:
        logger.error(f"Error classifying attempt: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to classify error: {str(e)}"
        )

@router.get("/model-info", response_model=ModelInfoResponse, summary="Retrieve Error Classifier metadata")
def model_info(
    error_service: ErrorClassifierService = Depends(get_error_classifier_service)
):
    """
    Returns metadata about the deployed Error Classifier model.
    """
    try:
        return error_service.get_model_info()
    except Exception as e:
        logger.error(f"Error fetching model info: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch model info: {str(e)}"
        )

@router.post("/classify-concept", response_model=ConceptClassificationResponse, summary="Classify concept using embedding & graph")
def classify_concept(
    request: ConceptClassificationRequest,
    concept_service: ConceptEngineService = Depends(get_concept_engine_service)
):
    """
    Identifies the underlying mathematical concept using embedding-based similarity retrieval + Knowledge Graph.
    """
    try:
        return concept_service.identify_concept(
            question=request.question,
            student_answer=request.student_answer,
            work_evidence=request.work_evidence or "",
            error_type=request.error_type
        )
    except Exception as e:
        logger.error(f"Error classifying concept: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to classify concept: {str(e)}"
        )

@router.post("/analyze-attempt", response_model=AttemptAnalysisResponse, summary="End-to-End student attempt diagnostic pipeline")
def analyze_attempt(
    request: AttemptAnalysisRequest,
    error_service: ErrorClassifierService = Depends(get_error_classifier_service),
    concept_service: ConceptEngineService = Depends(get_concept_engine_service)
):
    """
    Complete MindTrace AI pipeline:
    1. Error Classifier (Why did student fail?)
    2. Concept Engine + Knowledge Graph (What concept is involved & where does it belong?)
    """
    try:
        # Step 1: Error Classification
        err_req = ErrorClassificationRequest(
            question=request.question,
            correct_answer=request.correct_answer,
            student_answer=request.student_answer,
            work_evidence=request.work_evidence or ""
        )
        err_res = error_service.classify_error(err_req)

        # Step 2: Concept Engine Classification
        concept_res = concept_service.identify_concept(
            question=request.question,
            student_answer=request.student_answer,
            work_evidence=request.work_evidence or "",
            error_type=err_res.error_type
        )

        return AttemptAnalysisResponse(
            error=ErrorDetail(
                type=err_res.error_type,
                confidence=err_res.confidence
            ),
            concept=ConceptDetail(
                name=concept_res.concept,
                confidence=concept_res.confidence
            ),
            hierarchy=concept_res.hierarchy,
            prerequisites=concept_res.prerequisites,
            related_concepts=concept_res.related_concepts
        )
    except Exception as e:
        logger.error(f"Error executing end-to-end attempt analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform attempt analysis: {str(e)}"
        )
