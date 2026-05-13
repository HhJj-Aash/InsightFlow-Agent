import sys
from dotenv import load_dotenv
from agents.controller_agent import run_pipeline

load_dotenv()

if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_data.csv"
    try:
        report = run_pipeline(data_path)
        print(f"Report generated: {report}")
    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)
