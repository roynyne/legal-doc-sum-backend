from fastapi import APIRouter, UploadFile, File
from app.utils.file_loader import preprocess_case
from app.utils.structured_summary import structured_summary_pipeline
from app.utils.evaluation import catchphrase_coverage, compression_ratio
import tempfile

router = APIRouter()

@router.post("/structured")
async def summarize_structured(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    case_data = preprocess_case(tmp_path)

    if "error" in case_data:
        return case_data

    structured = structured_summary_pipeline(
        case_data["sentences"],
        catchphrases=case_data["catchphrases"],
        top_k=5
    )

    # Combine all abstracts into one text to compute evaluation metrics
    all_summary_text = list(structured.values())

    coverage, matched = catchphrase_coverage(all_summary_text, case_data["catchphrases"])
    compression = compression_ratio(all_summary_text, case_data["sentences"])

    return {
        "case_name": case_data["case_name"],
        "structured_summary": structured,
        "evaluation": {
            "catchphrase_coverage_ratio": round(coverage, 3),
            "matched_catchphrases": matched,
            "compression_ratio": round(compression, 3)
        }
    }
