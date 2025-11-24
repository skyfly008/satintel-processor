from typing import List


def fetch_dynamic_imagery(area_id: str, date: str) -> str:
    # placeholder: return path to a static sample image or a generated filename
    return f"data/imagery/{area_id}/{date}.png"


def batch_fetch(tasks: List[dict]) -> List[str]:
    # Accepts list of {area_id, date}
    return [fetch_dynamic_imagery(t["area_id"], t["date"]) for t in tasks]
