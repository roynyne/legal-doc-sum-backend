import re
import html
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union, List, Dict


def load_and_fix_xml(file_path: Union[str, Path]) -> ET.Element:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_xml = f.read()

    raw_xml = re.sub(r'<catchphrase\s+"id=([^"]+)"', r'<catchphrase id="\1"', raw_xml)
    raw_xml = raw_xml.replace("’", "'").replace("‘", "'")
    raw_xml = raw_xml.replace("–", "-").replace("—", "-")
    raw_xml = raw_xml.replace("“", '"').replace("”", '"')
    raw_xml = html.unescape(raw_xml)
    raw_xml = re.sub(r'&(?!amp;|lt;|gt;|apos;|quot;|#\d+;)', '&amp;', raw_xml)

    return ET.fromstring(raw_xml)


def clean_sentence(sentence: str) -> str:
    # Remove leading numbering like "1.", "3.1.2.", etc.
    sentence = re.sub(r'^\s*\d+(\.\d+)*\.?\s*', '', sentence)

    # Remove tags like [sic] and other bracketed expressions
    sentence = re.sub(r'\[sic\]|\[.*?\]', '', sentence)

    # Remove leading/trailing quotes or extra dots
    sentence = sentence.strip('"').strip("'").strip()
    sentence = re.sub(r'^\.*|\.*$', '', sentence)

    # Collapse whitespace
    sentence = re.sub(r'\s+', ' ', sentence)

    # Remove boilerplate/legal footer type lines
    boilerplate_keywords = [
        "certify", "counsel for", "solicitor for", "dated:",
        "austlii", "URL: http", "feedback", "privacy policy"
    ]
    if any(kw in sentence.lower() for kw in boilerplate_keywords):
        return ""

    # Remove short/uninformative or symbol-only lines
    if len(sentence.split()) < 4:
        return ""

    # Remove lines that are just numbers, letters or punctuation
    if re.fullmatch(r"[0-9a-zA-Z\s\.\-]+", sentence) and len(sentence.strip()) < 10:
        return ""

    # !!NEW: Remove long sentences!!
    if len(sentence.split()) > 100:
        return ""
    
    return sentence


def parse_case(root: ET.Element) -> Dict[str, List[str]]:
    case_name = root.find("name").text.strip()

    # Extract catchphrases
    catchphrases = []
    catchphrase_root = root.find("catchphrases")
    if catchphrase_root is not None:
        catchphrases = [
            cp.text.strip() for cp in catchphrase_root.findall("catchphrase") if cp.text
        ]

    # Extract and clean sentences
    sentences = []
    sentence_root = root.find("sentences")
    if sentence_root is not None:
        for s in sentence_root.findall("sentence"):
            if s.text:
                cleaned = clean_sentence(s.text.strip())
                if cleaned:
                    sentences.append(cleaned)

    return {
        "case_name": case_name,
        "catchphrases": catchphrases,
        "sentences": sentences,
    }


def preprocess_case(file_path: Union[str, Path]) -> Dict:
    try:
        root = load_and_fix_xml(file_path)
        case_data = parse_case(root)
        case_data["file"] = Path(file_path).name
        return case_data
    except Exception as e:
        return {
            "file": Path(file_path).name,
            "error": str(e)
        }
