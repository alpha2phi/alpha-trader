from typing import List
from ..data.schemas import ShortPremiumIdea

def short_premium_table(ideas: List[ShortPremiumIdea]) -> str:
    header = "| Ticker | Strategy | POP (%) | Max Profit ($) / Max Loss ($) | Notes |\n|--------|----------|---------|-------------------------------|-------|"
    rows = []
    for i in ideas:
        pop = f"{i.pop:.0f}" if i.pop is not None else "N/A"
        prof_loss = f"${i.max_profit:.0f} / ${i.max_loss:.0f}" if (i.max_profit is not None and i.max_loss is not None) else "N/A"
        rows.append(f"| {i.ticker} | {i.strategy} | {pop} | {prof_loss} | {i.notes} |")
    return "\n".join([header] + rows)

def long_term_table(candidates: List[tuple]) -> str:
    header = "| Ticker | Rationale | Suggested Allocation % |\n|--------|-----------|-----------------------|"
    rows = []
    if not candidates:
        rows.append("|  | No candidates today. |  |")
    else:
        for tkr, why, alloc in candidates:
            rows.append(f"| {tkr} | {why} | {alloc} |")
    return "\n".join([header] + rows)
