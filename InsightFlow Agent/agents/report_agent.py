from llm.llm_client import call_llm
from utils.file_utils import read_prompt, save_file
import os
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_report(analysis: dict, charts: list, output_path: str = "outputs/report.md") -> str:
    try:
        prompt_template = read_prompt("report_prompt")
        chart_names = "\n".join([os.path.basename(p) for p in charts]) if charts else "No charts generated"
        prompt = prompt_template.format(
            analysis=analysis.get("analysis", "No analysis available"),
            charts=chart_names
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load report prompt: {e}")

    try:
        logger.info("Generating report via LLM")
        text = call_llm(prompt)
    except Exception as e:
        raise RuntimeError(f"LLM report generation failed: {e}")

    try:
        save_file(text, output_path)
        logger.info(f"Report saved to {output_path}")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to save report: {e}")
