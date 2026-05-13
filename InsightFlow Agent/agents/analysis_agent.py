from llm.llm_client import call_llm
from utils.file_utils import read_prompt
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

def analyze_with_llm(df, max_rows: int = 10) -> dict:
    try:
        sample = df.head(max_rows).to_string()
        logger.info(f"Analyzing data sample ({max_rows} rows)")
    except Exception as e:
        raise RuntimeError(f"Failed to prepare data sample: {e}")

    try:
        prompt_template = read_prompt("analysis_prompt")
        prompt = prompt_template.format(data=sample)
    except Exception as e:
        raise RuntimeError(f"Failed to load analysis prompt: {e}")

    try:
        result = call_llm(prompt)
        return {"analysis": result}
    except Exception as e:
        raise RuntimeError(f"LLM analysis failed: {e}")
