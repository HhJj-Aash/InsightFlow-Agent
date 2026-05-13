import matplotlib.pyplot as plt
import os
import logging
from utils.logger import get_logger
from utils.file_utils import ensure_dir

logger = get_logger(__name__)

def generate_charts(df, output_dir: str = "outputs/charts") -> list:
    try:
        ensure_dir(output_dir)
        paths = []
        num_cols = df.select_dtypes(include="number").columns

        if len(num_cols) == 0:
            logger.warning("No numeric columns found for chart generation")
            return paths

        for col in num_cols:
            try:
                plt.figure()
                df[col].plot(title=col)
                path = os.path.join(output_dir, f"{col}.png")
                plt.savefig(path, dpi=100, bbox_inches="tight")
                plt.close()
                paths.append(path)
                logger.info(f"Generated chart: {path}")
            except Exception as e:
                logger.warning(f"Failed to generate chart for {col}: {e}")
                plt.close()

        return paths
    except Exception as e:
        raise RuntimeError(f"Chart generation failed: {e}")
