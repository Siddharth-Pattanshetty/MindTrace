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
    ConceptDetail,
    MasteryDetail,
    RootCauseDetail,
    RecommendationDetail
)
from app.ai.mastery.service import MasteryService, get_mastery_service
from app.ai.mastery.schemas import MasteryPredictionRequest, MasteryPredictionResponse
from app.ai.root_cause.service import RootCauseService, get_root_cause_service
from app.ai.root_cause.schemas import RootCausePredictionRequest, RootCausePredictionResponse

logger = logging.getLogger("mindtrace.api.ai")

router = APIRouter()

@router.post("/classify-error", response_model=ErrorClassificationResponse, summary="Classify student error type")
def classify_error(
    request: ErrorClassificationRequest,
    error_service: ErrorClassifierService = Depends(get_error_classifier_service)
):
    try:
        return error_service.classify_error(request)
    except Exception as e:
        logger.error(f"Error classifying attempt: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to classify error: {str(e)}"
        )

@router.post("/classify-concept", response_model=ConceptClassificationResponse, summary="Classify concept using embedding & graph")
def classify_concept(
    request: ConceptClassificationRequest,
    concept_service: ConceptEngineService = Depends(get_concept_engine_service)
):
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

@router.post("/predict-mastery", response_model=MasteryPredictionResponse, summary="Predict student mastery probability of success")
def predict_mastery(
    request: MasteryPredictionRequest,
    mastery_service: MasteryService = Depends(get_mastery_service)
):
    try:
        return mastery_service.predict_mastery(request)
    except Exception as e:
        logger.error(f"Error predicting mastery: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict mastery: {str(e)}"
        )

@router.post("/predict-root-cause", response_model=RootCausePredictionResponse, summary="Predict Root Cause with Confidence Calibration")
def predict_root_cause(
    request: RootCausePredictionRequest,
    root_cause_service: RootCauseService = Depends(get_root_cause_service)
):
    try:
        return root_cause_service.predict_root_cause(request)
    except Exception as e:
        logger.error(f"Error predicting root cause: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict root cause: {str(e)}"
        )

@router.get("/model-info", response_model=ModelInfoResponse, summary="Retrieve AI Pipeline metadata")
def model_info(
    error_service: ErrorClassifierService = Depends(get_error_classifier_service),
    mastery_service: MasteryService = Depends(get_mastery_service),
    root_cause_service: RootCauseService = Depends(get_root_cause_service)
):
    try:
        err_info = error_service.get_model_info()
        mastery_info = mastery_service.get_model_info()
        rc_info = root_cause_service.get_model_info()

        return ModelInfoResponse(
            error_classifier=err_info,
            mastery_model=mastery_info,
            root_cause_model=rc_info.get("root_cause_model"),
            confidence_calibration=rc_info.get("confidence_calibrator"),
            model_name="MindTrace Mathematics AI Diagnostic Pipeline V1",
            version="1.0.0",
            algorithm="TF-IDF + Logistic Regression (Error), XGBoost (Mastery), Random Forest + Platt Calibration (Root Cause)",
            dataset="MAP & ASSISTments & MindTrace Root Cause Dataset V1"
        )
    except Exception as e:
        logger.error(f"Error fetching model info: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch model info: {str(e)}"
        )

@router.post("/analyze-attempt", response_model=AttemptAnalysisResponse, summary="End-to-End student attempt diagnostic pipeline")
def analyze_attempt(
    request: AttemptAnalysisRequest,
    error_service: ErrorClassifierService = Depends(get_error_classifier_service),
    concept_service: ConceptEngineService = Depends(get_concept_engine_service),
    mastery_service: MasteryService = Depends(get_mastery_service),
    root_cause_service: RootCauseService = Depends(get_root_cause_service)
):
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

        # Step 3: Mastery Model Prediction
        mastery_req = MasteryPredictionRequest(
            student_id=request.student_id,
            concept=concept_res.concept
        )
        mastery_res = mastery_service.predict_mastery(mastery_req)

        # Step 4: Root Cause Prediction & Confidence Calibration
        rc_req = RootCausePredictionRequest(
            student_id=request.student_id,
            subject=request.subject,
            question=request.question,
            correct_answer=request.correct_answer,
            student_answer=request.student_answer,
            work_evidence=request.work_evidence,
            error_type=err_res.error_type,
            concept=concept_res.concept,
            error_confidence=err_res.confidence,
            concept_confidence=concept_res.confidence,
            concept_mastery=mastery_res.mastery
        )
        rc_res = root_cause_service.predict_root_cause(rc_req)

        # Step 5: Recommendation Engine Mapping
        rec_action = f"Remediate {rc_res.root_cause.replace('_', ' ').title()}"
        rec_reason = f"Identified {err_res.error_type} in {concept_res.concept} driven by {rc_res.root_cause} with {rc_res.calibrated_probability*100:.1f}% calibrated confidence (Mastery: {mastery_res.mastery*100:.1f}%)."
        suggested = concept_res.prerequisites if concept_res.prerequisites else [concept_res.concept]

        rec_detail = RecommendationDetail(
            action=rec_action,
            target_concept=concept_res.concept,
            reasoning=rec_reason,
            suggested_practice_topics=suggested
        )

        err_detail = ErrorDetail(
            type=err_res.error_type,
            confidence=round(err_res.confidence, 4)
        )

        mastery_detail = MasteryDetail(
            concept=concept_res.concept,
            mastery=mastery_res.mastery,
            probability_of_success=mastery_res.probability_of_success,
            trend=mastery_res.trend
        )

        return AttemptAnalysisResponse(
            subject=request.subject,
            error_type=err_res.error_type,
            error_confidence=round(err_res.confidence, 4),
            concept=concept_res.concept,
            concept_confidence=round(concept_res.confidence, 4),
            root_cause=rc_res.root_cause,
            root_cause_probability=rc_res.calibrated_probability,
            raw_root_cause_probability=rc_res.raw_probability,
            calibration_method=rc_res.calibration_method,
            error=err_detail,
            error_detail=err_detail,
            concept_detail=ConceptDetail(
                name=concept_res.concept,
                confidence=round(concept_res.confidence, 4)
            ),
            mastery=mastery_detail,
            root_cause_detail=RootCauseDetail(
                root_cause=rc_res.root_cause,
                calibrated_probability=rc_res.calibrated_probability,
                raw_probability=rc_res.raw_probability,
                calibration_method=rc_res.calibration_method
            ),
            recommendation=rec_detail,
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
