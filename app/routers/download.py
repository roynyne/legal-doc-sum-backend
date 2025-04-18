from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import FileResponse, PlainTextResponse
from app.exporters.pdf_exporter import generate_pdf
from app.exporters.word_exporter import generate_docx
from app.exporters.markdown_exporter import generate_markdown
from app.utils.file_loader import preprocess_case
from app.utils.structured_summary import structured_summary_pipeline
from app.utils.evaluation import catchphrase_coverage, compression_ratio
import tempfile

# ✅ Declare the router
router = APIRouter()

@router.post("/brief")
async def download_case_brief(file: UploadFile = File(...), format: str = Query("md")):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    case = preprocess_case(tmp_path)
    if "error" in case:
        return case

    structured = structured_summary_pipeline(
        case["sentences"],
        catchphrases=case["catchphrases"]
    )
    all_text = list(structured.values())
    coverage, matched = catchphrase_coverage(all_text, case["catchphrases"])
    compression = compression_ratio(all_text, case["sentences"])

    case_data = {
        "case_name": case["case_name"],
        "structured_summary": structured,
        "evaluation": {
            "catchphrase_coverage_ratio": coverage,
            "matched_catchphrases": matched,
            "compression_ratio": compression
        }
    }

    if format == "md":
        markdown = generate_markdown(case_data)
        return PlainTextResponse(markdown, media_type="text/markdown")

    elif format == "pdf":
        generate_pdf(case_data, tmp_path)
        return FileResponse(tmp_path, media_type="application/pdf", filename="case_brief.pdf")

    elif format == "docx":
        generate_docx(case_data, tmp_path)
        return FileResponse(
            tmp_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="case_brief.docx"
        )

    return {"error": "Supported formats: md, pdf, docx"}
