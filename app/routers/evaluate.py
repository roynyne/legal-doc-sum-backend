from fastapi import APIRouter, UploadFile, File
from app.utils.file_loader import preprocess_case
from app.models.extractive_legalbert import advanced_extractive_summary
from app.utils.evaluation import catchphrase_coverage, compression_ratio
import tempfile

router = APIRouter()

@router.post("/extractive")
async def evaluate_extractive_summary(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    case_data = preprocess_case(tmp_path)

    if "error" in case_data:
        return case_data

    summary = advanced_extractive_summary(
        case_data["sentences"],
        catchphrases=case_data["catchphrases"],
        top_k=5
    )

    coverage, matched = catchphrase_coverage(summary, case_data["catchphrases"])
    compression = compression_ratio(summary, case_data["sentences"])

    return {
        "case_name": case_data["case_name"],
        "summary_sentences": summary,
        "metrics": {
            "catchphrase_coverage_ratio": round(coverage, 3),
            "matched_catchphrases": matched,
            "compression_ratio": round(compression, 3)
        }
    }
