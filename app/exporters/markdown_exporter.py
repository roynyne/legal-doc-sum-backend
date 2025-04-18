def generate_markdown(case_data: dict) -> str:
    case_name = case_data["case_name"]
    sections = case_data["structured_summary"]
    evaluation = case_data.get("evaluation", {})

    md = [f"# 📄 Case Brief: {case_name}", ""]

    for section, text in sections.items():
        title = section.capitalize()
        md.append(f"## {title}\n{text}\n")

    if evaluation:
        md.append("---\n")
        md.append("### 📊 Evaluation")
        for metric, val in evaluation.items():
            if isinstance(val, float):
                val = f"{val:.2f}"
            md.append(f"- **{metric.replace('_', ' ').title()}**: {val}")

    return "\n".join(md)
