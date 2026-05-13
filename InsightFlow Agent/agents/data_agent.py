import pandas as pd
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

def load_and_clean(file_path: str, drop_na: bool = False, fill_strategy: str = "mean") -> pd.DataFrame:
    try:
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {e}")

    df.columns = [c.lower().strip() for c in df.columns]

    if drop_na:
        df = df.dropna()
        logger.info(f"After dropping NA: {len(df)} rows")
    else:
        num_cols = df.select_dtypes(include="number").columns
        if fill_strategy == "mean":
            df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
        elif fill_strategy == "median":
            df[num_cols] = df[num_cols].fillna(df[num_cols].median())
        elif fill_strategy == "forward":
            df = df.fillna(method="ffill")
        logger.info(f"Filled missing values using {fill_strategy} strategy")

    return df
