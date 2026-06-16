from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_generation_and_validation():
    subprocess.run([sys.executable, "scripts/generate_synthetic_cruise_data.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/validate_generated_data.py"], cwd=ROOT, check=True)
    assert (ROOT / "data" / "raw" / "reservations.csv").exists()
    assert (ROOT / "dbt_cruise_analytics" / "seeds" / "reservations.csv").exists()
