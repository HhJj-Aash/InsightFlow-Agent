from agents.data_agent import load_and_clean
from agents.analysis_agent import analyze_with_llm
from agents.viz_agent import generate_charts
from agents.report_agent import generate_report
from utils.logger import get_logger

logger = get_logger(__name__)

def run_pipeline(file_path: str, fill_strategy: str = "mean") -> str:
    logger.info("Controller Agent starting")

    try:
        logger.info("Data Agent: Loading and cleaning data")
        data = load_and_clean(file_path, fill_strategy=fill_strategy)
    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        raise

    try:
        logger.info("Analysis Agent: LLM analysis")
        analysis = analyze_with_llm(data)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

    try:
        logger.info("Visualization Agent: Generating charts")
        charts = generate_charts(data)
    except Exception as e:
        logger.warning(f"Visualization failed, continuing without charts: {e}")
        charts = []

    try:
        logger.info("Report Agent: Generating report")
        report_path = generate_report(analysis, charts)
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise

    logger.info("Pipeline completed successfully")
    return report_path
