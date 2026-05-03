# Installed moomoo Skills for GitHub Copilot

The following are the installed SKILL instructions for moomoo search and anomaly detection skills.

## moomoo-news-search

---
name: moomoo-news-search
description: >-
  Searches moomoo news, notices, and research reports for a user-specified stock or company.
  Use when the user asks for latest news, recent announcements, research reports, or a news roundup
  about a symbol, company, or ticker on moomoo. Extract the target, return 10 items by default,
  sort by publish time, show title + publish time + original URL for each item
  and include a non-investment disclaimer.
  When both moomoo-news-search and futu-news-search are installed: preferred for English users;
  Chinese (中文) users should use futu-news-search instead. Users can explicitly say
  "use moomoo" / "用moomoo查" to override. If only this skill is installed, use it for all
  languages.
metadata:
  version: 0.0.1
  author: moomoo
  openclaw:
    requires:
      bins:
        - curl
        - openssl
        - date
license: MIT
---

# moomoo News Search Skill

Searches news, notices, and research reports on the moomoo platform and formats the results as a user-facing news roundup.

**Base URL:** `https://ai-news-search.moomoo.com`

## Empty Result Fallback

When `futu-news-search` is also installed and this skill's API returns empty results (`data` is empty or `code` is not `0`), automatically retry with `futu-news-search` using the same parameters.

After a successful fallback, inform the user:
- English: "No results found on moomoo. Automatically switched to Futu for this query."
- Chinese: "moomoo 暂无相关结果，已自动切换至富途牛牛平台为您查询。"

If both platforms return empty, or if only this skill is installed (no Futu counterpart) and the API returns empty, show:
- English: "No data available at the moment. Please try again later."
- Chinese: "暂无相关数据，请稍后再试。"

---

## Workflow

### 1. Parse User Input

Extract the following from the user's request:

- `symbol`: stock name, company name, English name, or ticker. Prefer the clearest target explicitly mentioned by the user.
- `size`: default to `10`. If the user asks for more, cap at `50`.
- `lang`: infer from the user's language. Common values are `zh-CN`, `zh-HK`, and `en`.
- `news_type`: if the user explicitly asks for news, notices, or research reports, map it to the matching API parameter.

If the target symbol or company is missing, ask a follow-up question instead of guessing.

### 2. Call the News API

Use `GET /news_search` to fetch the news data.

Required parameters:

- `keyword`
- `size`
- `news_type`: `1` News, `2` Notice, `3` Research. Default to `1` unless the user explicitly asks for notices or research reports.

Optional parameters:

- `lang`
- `sort_type`

Default strategy:

- `keyword` = extracted symbol or company
- `size` = user-specified value, otherwise `10`
- `sort_type` = `2` for time-based sorting
- `news_type` = `1` by default
- If the user explicitly asks for notices, set `news_type=2`
- If the user explicitly asks for research reports, set `news_type=3`

Request example:

```bash
curl -sG 'https://ai-news-search.moomoo.com/news_search' \
  -H 'User-Agent: moomoo-news-search/0.0.2 (Skill)' \
  --data-urlencode 'keyword=Tencent' \
  --data-urlencode 'size=10' \
  --data-urlencode 'news_type=1' \
  --data-urlencode 'lang=en' \
  --data-urlencode 'sort_type=2'
```

### 3. Filter and Sort Results

- After the API call, check whether `code` is `0`. If not, surface the error message and do not fabricate results.
- If the result set is empty, clearly tell the user that no relevant items were found.
- Present the final list in reverse chronological order, newest first.

### 4. Organize the Information

For each item, include:

- title
- publish time
- original link

Publish time requirements:

- Prefer converting `publish_time` into a human-readable local time before replying.
- If the API returns a Unix timestamp in seconds, format it as `YYYY-MM-DD HH:mm:ss`.
- If the API returns a Unix timestamp in milliseconds, convert it first, then format it as `YYYY-MM-DD HH:mm:ss`.
- If the exact timezone is unclear, label it conservatively as `publish time` and do not invent a timezone abbreviation.

### 5. Return Structured Output

Use the following default template:

```markdown
{{symbol}} latest news (sorted by time):

1. {{title_1}}
Publish time: {{publish_time_1}}
URL: {{url_1}}

2. {{title_2}}
Publish time: {{publish_time_2}}
URL: {{url_2}}

...

10. {{title_10}}
Publish time: {{publish_time_10}}
URL: {{url_10}}

The above content is compiled from public information and does not constitute investment advice.

{{platform_source_footer}}
```

Output requirements:

- Always preserve the original article URL.
- Always show the title, publish time, and URL for every returned item.
- Do not show raw JSON by default.
- If fewer items are returned than requested, show only the actual items and do not pad the list.

### 6. Disclaimer

Append the following line at the end of every result:

`The above content is compiled from public information and does not constitute investment advice.`

### 7. Platform Source Footer

When both `moomoo-news-search` and `futu-news-search` are installed, append a platform source line after the disclaimer, matching the user's language:

- English: `Source: moomoo | English queries default to moomoo; Chinese queries default to Futu. Say "use futu" to switch.`
- Chinese: `数据来源：moomoo | 英文默认使用 moomoo，中文默认使用牛牛。输入「用牛牛查」可切换平台。`

If only this skill is installed (no Futu counterpart), do not show the platform source footer.

## API Reference

### Endpoint

- `GET /news_search`

### Parameters

- `keyword`: search keyword, must not be empty
- `size`: number of items to return, must be greater than `0`, maximum `50`
- `news_type`: `1` News, `2` Notice, `3` Research
- `lang`: `zh-CN`, `zh-HK`, `en`
- `sort_type`: `1` by popularity, `2` by time, `3` by attention

### Response Shape

Top-level fields:

- `code`: `0` means success
- `message`: error message
- `data`: result array

Common item fields:

- `news_id`
- `news_type`
- `title`
- `publish_time`
- `url`
- `img_url`

## Behavior Rules

1. When the user asks for "latest news", "recent updates", or a news roundup, default to `10` items + `sort_type=2` + `news_type=1`.
2. When the user asks specifically for notices, prefer `news_type=2`. For research reports, prefer `news_type=3`.
3. If the user provides only a company name, use it directly as `keyword`. If the user provides a ticker, try the ticker first, and if needed retry once with a more natural company-name query.
4. Do not interpret the results as investment advice, trading signals, or target-price guidance.
5. Do not invent sources, timestamps, or links.
6. If `publish_time` is present, include it in every item rather than omitting it.
7. Do not omit `news_type` in default requests, because default behavior should focus on actual news items only.

## Example

```markdown
Tencent latest news (sorted by time):

1. Tencent short-selling volume surged 266% during the March Hong Kong market pullback
Publish time: 2026-03-31 09:30:00
URL: https://...

2. Tencent completed buybacks for three consecutive days, totaling about HKD 900 million
Publish time: 2026-03-30 18:12:00
URL: https://...

3. Southbound funds posted net buying in Tencent for three straight days
Publish time: 2026-03-30 15:48:00
URL: https://...

The above content is compiled from public information and does not constitute investment advice.

Source: moomoo | English queries default to moomoo; Chinese queries default to Futu. Say "use futu" to switch.
```

## Security

- Do not expose internal authentication details, cookies, tokens, or gateway internals in the reply.
- Use `--data-urlencode` for `keyword` so Chinese text and special characters are encoded correctly.

## moomoo-stock-digest

---
name: moomoo-stock-digest
description: >-
  Interprets the latest public news for one user-specified stock or company by
  calling the moomoo news search API directly, extracting key events, judging likely impact
  direction, and returning a structured stock digest with evidence links and a
  non-investment disclaimer. Use when the user asks for a stock digest,
  single-stock news interpretation, stock news interpretation, or moomoo stock
  digest.
  When both moomoo-stock-digest and futu-stock-digest are installed: preferred for English users;
  Chinese (中文) users should use futu-stock-digest instead. Users can explicitly say
  "use moomoo" / "用moomoo查" to override. If only this skill is installed, use it for all
  languages.
metadata:
  version: 0.0.2
  author: moomoo
  openclaw:
    requires:
      bins:
        - curl
        - openssl
        - date
license: MIT
---

# moomoo Stock Digest Skill

Structured **single-stock news interpretation workflow** on the moomoo platform.

This skill accepts **one target only**, such as a stock name, company name, or ticker-like symbol string. It does not decide the target on its own. The caller must supply the stock to interpret.

The skill orchestrates:

1. parse the user's target symbol
2. call `GET /news_search` on `https://ai-news-search.moomoo.com` directly to obtain the latest public news
3. extract the key events from the returned items
4. judge the overall direction as `bullish` / `bearish` / `neutral`
5. organize the result into a fixed user-facing digest template
6. append a mandatory disclaimer

**Base URL:** `https://ai-news-search.moomoo.com`

---

## Empty Result Fallback

When `futu-stock-digest` is also installed and this skill's API returns empty results (`data` is empty or `code` is not `0`), automatically retry with `futu-stock-digest` using the same parameters.

After a successful fallback, inform the user:
- English: "No news data found on moomoo. Automatically switched to Futu for this digest."
- Chinese: "moomoo 暂无相关新闻数据，已自动切换至富途牛牛平台为您解读。"

If both platforms return empty, or if only this skill is installed (no Futu counterpart) and the API returns empty, show:
- English: "No data available at the moment. Please try again later."
- Chinese: "暂无相关数据，请稍后再试。"

---

## When to Use

| Scenario | Reason |
| -------- | ------ |
| User wants a stock digest | This skill converts the latest related news into a concise single-stock interpretation. |
| User asks for a single-stock interpretation | It turns recent public information into a conclusion, signals, and evidence. |
| User wants a fast directional read | It labels the overall tone as `bullish` / `bearish` / `neutral` based on retrieved items. |
| User wants evidence-backed output | It keeps original titles and links for auditability. |

**Not a fit:** portfolio construction, multi-stock watchlist batching, valuation modeling, price targets, or investment advice.

---

## Scope Boundary

This skill is intentionally narrow:

* **Input owned by caller:** one stock / company / symbol only
* **Retrieval owned by this skill:** call `GET /news_search` directly
* **Interpretation owned by this skill:** summarize key events, infer direction, and produce the fixed digest

Do not add logic here for:

* deriving the stock from a portfolio screenshot or holdings table
* brokerage account reads
* broad market strategy conclusions
* autonomous trading advice

If the caller provides:

* `Tencent` or `0700.HK` -> proceed
* multiple symbols in one request -> ask the caller to narrow it to one stock unless they explicitly ask for multiple separate digests
* a portfolio screenshot or holdings table -> ask the caller to first specify the target stock

---

## Quick Reference

| Step | Method | Purpose |
| ---- | ------ | ------- |
| 1 | Parse user request | Extract `symbol` |
| 2 | Call `GET /news_search` directly | Retrieve latest related public news |
| 3 | Event extraction | Summarize major new developments |
| 4 | Direction judgment | Classify overall tone as `bullish` / `bearish` / `neutral` |
| 5 | Fixed template rendering | Return conclusion, signals, and evidence links |

---

## Inputs

### Required

* **symbol**: One stock or company target, for example `Tencent`, `0700.HK`, `NVDA`, or `Apple`.

### Optional retrieval controls

* **size**: Number of news items to fetch from the API. Default `10`. Clamp to `3-20` unless the caller explicitly asks otherwise.
* **news_type**: Optional channel filter. Values: `1` News, `2` Notice, `3` Research.
* **lang**: Optional language for the API request. Common values: `zh-CN`, `zh-HK`, `en`.
* **sort_type**: Optional result order. Default `2` for time-based sorting.

### Validation Rules

| Check | Rule |
| ----- | ---- |
| `symbol` missing | Ask a follow-up question instead of guessing. |
| `symbol` empty after trim | Reject and ask for a valid stock or company target. |
| Multiple unrelated symbols detected | Ask the caller to choose one target. |
| `size < 1` | Reject and ask for a positive integer. |
| `size > 20` | Clamp to `20` with note unless the caller explicitly asks otherwise. |

---

## News API

This skill calls `GET /news_search` on `https://ai-news-search.moomoo.com` directly.

### Endpoint

- `GET /news_search`

### Parameters

- `keyword`: the resolved symbol or company name, must not be empty
- `size`: number of items to return, must be greater than `0`, maximum `50`
- `news_type`: `1` News, `2` Notice, `3` Research
- `lang`: `zh-CN`, `zh-HK`, `en`
- `sort_type`: `1` by popularity, `2` by time, `3` by attention

### Response Shape

Top-level fields:

- `code`: `0` means success
- `message`: error message
- `data`: result array

Common item fields:

- `news_id`
- `news_type`
- `title`
- `publish_time`
- `url`
- `img_url`

If `code` is not `0` or `data` is empty, do not fabricate interpretation. Use the empty-result fallback defined below.

## Skill Workflow

### 1. Parse User Input

Extract:

* `symbol`: the user's target stock, company, or ticker-like identifier

If no clear target is present, ask a follow-up question instead of guessing.

### 2. Call the News API

Call `GET /news_search` on `https://ai-news-search.moomoo.com` directly to retrieve the latest related public information for the target.

Default behavior:

* `keyword` = resolved symbol or company name
* `size=10`
* `news_type=1` (News) by default; set `2` for notices, `3` for research reports only when explicitly requested
* `sort_type=2` for time-based sorting
* infer `lang` from the user's language

Request example:

```bash
curl -sG 'https://ai-news-search.moomoo.com/news_search' \
  -H 'User-Agent: moomoo-stock-digest/0.0.2 (Skill)' \
  --data-urlencode 'keyword=Tencent' \
  --data-urlencode 'size=10' \
  --data-urlencode 'news_type=1' \
  --data-urlencode 'lang=en' \
  --data-urlencode 'sort_type=2'
```

After the API call:

* Check that `code` is `0`. If not, surface the error message and do not fabricate results.
* If `data` is empty, proceed to the empty-result fallback.
* Use `publish_time` for reference only; do not display raw news items in the final digest output.

### 3. Process the Information

From the retrieved items:

1. identify the latest high-signal events
2. collapse duplicates or near-duplicate headlines into one event
3. extract the most decision-relevant facts
4. judge the **overall direction**:
   * `bullish`: evidence is mostly supportive or positive for the stock
   * `bearish`: evidence is mostly negative or adverse
   * `neutral`: evidence is mixed, low-signal, or does not clearly change the outlook

Direction judgment should be conservative. If the evidence is mixed, default to `neutral` and explain the tension in the conclusion.

### 4. Organize the Information

Produce:

1. **Conclusion**: one short paragraph
2. **Key signals**: concise bullets based on the available high-signal information
3. **Key evidence**: highest-value original items with links

### 5. Return Structured Result

Render the fixed markdown template defined below. Prefer user-facing prose over raw JSON.

### 6. Add Disclaimer

Always append:

`This content is based on public information and does not constitute investment advice.`

### 7. Platform Source Footer

When both `moomoo-stock-digest` and `futu-stock-digest` are installed, append a platform source line after the disclaimer, matching the user's language:

- English: `Source: moomoo | English queries default to moomoo; Chinese queries default to Futu. Say "use futu" to switch.`
- Chinese: `数据来源：moomoo | 英文默认使用 moomoo，中文默认使用牛牛。输入「用牛牛查」可切换平台。`

If only this skill is installed (no Futu counterpart), do not show the platform source footer.

---

## Interpretation Policy

This skill is responsible for the final digest wording, but it must remain evidence-based and conservative.

The skill should therefore provide:

* explicit event extraction
* clear directional judgment
* fixed output structure
* auditable evidence links

The skill should **not**:

* invent facts not grounded in retrieved items
* give buy/sell/target-price advice
* overstate certainty when evidence is mixed or sparse

---

## Analysis Objectives

Analyze the retrieved items in this order:

1. identify the main event or topic
2. determine whether it is incremental new information or repeated noise
3. explain why it matters for the stock
4. judge the likely overall direction: `bullish` / `bearish` / `neutral`
5. extract the most important signals for the user
6. produce a concise, neutral stock digest

Do not skip directly from headline to conclusion without checking whether the evidence is repeated, weak, or mixed.

---

## Hard Constraints For Consistent Interpretation

Apply these constraints whenever generating the digest:

1. Base every claim on the retrieved news items first, background knowledge second.
2. Prefer newly disclosed events over generic company background.
3. When multiple items report the same event, merge them into one signal instead of repeating them.
4. If evidence is mixed, label the overall direction `neutral` unless one side clearly dominates.
5. Do not infer earnings, valuation, or target-price views unless directly supported by the retrieved items.
6. Do not use sensational or certainty-heavy language.
7. Do not provide trading instructions or investment advice.
8. Keep the conclusion to one paragraph and the signals concise.

---

## Output Template

Use the following default markdown template:

```markdown
{{symbol}} stock digest

Conclusion:
{{conclusion}}

Key signals:

- {{signal_1}}
- {{signal_2}}
- {{signal_3}}
- {{signal_4}}

Key evidence:

1. {{event_title_1}}
{{url_1}}

2. {{event_title_2}}
{{url_2}}

3. {{event_title_3}}
{{url_3}}

This content is based on public information and does not constitute investment advice.

{{platform_source_footer}}
```

Output requirements:

* `Conclusion` must be exactly one short paragraph.
* `Key signals` should contain as many items as needed to cover the meaningful signals without padding.
* `Key evidence` should include as many high-value original items as needed and must preserve the original links.
* If there is no meaningful new information, replace the evidence block with:

`No obvious new stock-specific factors were found.`

---

## User-Facing Example

```markdown
Tencent Holdings (0700.HK) stock digest

Conclusion:
Buybacks and continued southbound inflows provide support. Near-term volatility may remain elevated, but the overall funding picture is still constructive.

Key signals:

- Buybacks continued for three straight sessions, totaling about HKD 900 million
- Southbound funds kept recording net inflows
- Short interest increased, suggesting wider market disagreement
- AI and cloud initiatives continued to advance

Key evidence:

1. Tencent repurchased shares for three straight sessions, totaling about HKD 900 million
https://...

2. Southbound funds recorded net buying in Tencent for three consecutive days
https://...

3. Tencent short-selling volume surged 266% during the Hong Kong market pullback
https://...

This content is based on public information and does not constitute investment advice.

Source: moomoo | English queries default to moomoo; Chinese queries default to Futu. Say "use futu" to switch.
```

---

## Recommended Agent Workflow

When executing this skill, follow this checklist:

1. Validate that the caller supplied one target stock.
2. Normalize the target string without changing its meaning.
3. Call `GET /news_search` on `https://ai-news-search.moomoo.com` with the effective retrieval parameters.
4. If no relevant items are returned, explicitly say there are no obvious new factors.
5. Merge repeated headlines into consolidated events.
6. Extract the key signals that best reflect the available information.
7. Write one concise conclusion paragraph.
8. Select the strongest evidence items and preserve their original URLs.
9. Render the fixed template and append the disclaimer.

---

## User-Facing Output Guidance

When presenting results to the user in normal markdown:

1. Start directly with a localized title such as `{{symbol}} stock digest`.
2. Present the conclusion first, then signals, then evidence.
3. Localize section labels and the disclaimer to match the user's language when appropriate.
4. Keep the tone professional, concise, and evidence-based.
5. Preserve the original article titles and URLs in the evidence section.
6. If there is no meaningful new information, explicitly state `No obvious new stock-specific factors were found.`

Avoid:

* mixing unrelated old headlines into the digest just to fill the template
* treating generic market noise as stock-specific evidence
* implying that "no major new factor" means "no risk"

---

## Security

### Requests and Data

* Treat the target symbol as user input.
* Do not expose internal authentication details, cookies, or tokens.
* Preserve original URLs in output so the caller can audit the evidence.
* Do not invent missing links or source names.

### Disclaimer

* This skill is for public-information digestion only.
* Generated output is informational and is not investment advice.

---

## User Agent Header

Include a `User-Agent` header with the following string: `moomoo-stock-digest/0.0.2 (Skill)`

## moomoo-comment-sentiment

---
name: moomoo-comment-sentiment
description: >-
  Aggregates real-time moomoo community/feed discussions for one or more user-specified
  symbols, filters low-quality posts, classifies sentiment as bullish, bearish,
  or neutral, and returns a structured community sentiment snapshot for a single
  stock or a multi-symbol portfolio. Use when the user asks for stock community
  sentiment, retail discussion tone, portfolio sentiment snapshot, bullish vs
  bearish discussion, or moomoo-comment-sentiment.
  When both moomoo-comment-sentiment and futu-comment-sentiment are installed: preferred for
  English users; Chinese (中文) users should use futu-comment-sentiment instead. Users can
  explicitly say "use moomoo" / "用moomoo查" to override. If only this skill is installed,
  use it for all languages.
metadata:
  version: 0.0.2
  author: moomoo
  openclaw:
    requires:
      bins:
        - curl
        - openssl
        - date
license: MIT
---

# moomoo Comment Sentiment Skill

HTTP **single-symbol or multi-symbol real-time community sentiment aggregation** for discussions on the moomoo platform.

This skill is designed for user requests such as:

- "Check NVDA community sentiment"
- "Help me see whether Tesla comments in the last 24 hours are more bullish or bearish"
- "Analyze the community sentiment for this group of stocks"
- "Create a community sentiment summary for a US tech stock portfolio"

The skill retrieves recent community posts for each target symbol, filters low-quality content, computes bullish / bearish / neutral distribution, then produces:

1. single-symbol sentiment output when only one target is supplied
2. portfolio-level sentiment summary when multiple targets are supplied
3. top community opinions across the whole group
4. per-symbol sentiment breakdown for comparison

**Base URL:** `https://ai-news-search.moomoo.com`

---

## Empty Result Fallback

When `futu-comment-sentiment` is also installed and this skill's API returns empty results (`data` is empty or `code` is not `0`), automatically retry with `futu-comment-sentiment` using the same parameters.

After a successful fallback, inform the user:
- English: "No community data found on moomoo. Automatically switched to Futu for this query."
- Chinese: "moomoo 暂无相关社区讨论数据，已自动切换至富途牛牛平台为您查询。"

If both platforms return empty, or if only this skill is installed (no Futu counterpart) and the API returns empty, show:
- English: "No data available at the moment. Please try again later."
- Chinese: "暂无相关数据，请稍后再试。"

---

## Positioning

This skill focuses on **community discussion tone**, not fundamental valuation, not official filings, and not price prediction.

It should be used when the user wants:

- retail discussion mood
- community consensus vs disagreement
- quick symbol-by-symbol sentiment comparison
- a structured portfolio sentiment snapshot

It is **not** a fit for:

- official announcements only
- pure news roundup without community interpretation
- financial advice, target price, or trading execution

---

## Workflow

### 1. Parse User Input

Extract the following from the user's request:

- `symbol_list`: one or more symbols, company names, or recognizable stock aliases
- `group_name`: optional portfolio/group display name if the user provides one, for example `US Tech Portfolio`
- `lang`: infer from the user's language, typically `zh-CN`, `zh-HK`, or `en`

Parsing rules:

1. If no symbol can be identified, ask the user to provide at least one target.
2. If only one symbol is identified, run **single-symbol mode**.
3. If multiple symbols are identified, run **multi-symbol mode**.
4. Ignore user-provided time windows unless the upstream API explicitly supports them, because this skill is defined as a real-time snapshot workflow.

### 2. Call Community Data API

For each symbol in `symbol_list`, retrieve recent discussion/feed posts related to that symbol.

Preferred retrieval strategy:

1. Use the moomoo feed/community endpoint that returns recent stock-related discussion items.
2. Keep results in reverse chronological order.
3. Preserve upstream metadata per symbol.
4. If a symbol fails upstream, record the failure and continue processing other symbols instead of aborting the whole batch.

### 3. Information Processing

For each symbol separately:

1. Clean text:
   - strip HTML tags from title / desc
   - merge visible title + desc into one analysis text
2. Convert timestamps:
   - treat `publish_time` as a Unix epoch value (seconds); if it looks like milliseconds (> 1e12), divide by 1000
   - convert to a human-readable string in the format `YYYY-MM-DD HH:mm` using UTC+8 (Asia/Shanghai) unless the user's locale implies otherwise
   - store the converted string as `published_at` on each post
   - after processing all posts for a symbol, record `time_range_earliest` and `time_range_latest` from the full (pre-filter) batch so the header reflects the actual data window
3. Filter low-quality content:
   - remove spammy or near-empty text
   - remove obvious water posts / repeated filler phrases
   - down-weight or exclude posts with extremely weak information density
   - down-weight or exclude very low-interaction content when interaction signals are available
3. Classify each retained post:
   - `bullish`
   - `bearish`
   - `neutral`
4. Aggregate each symbol:
   - `bull_pct`
   - `bear_pct`
   - `neutral_pct`
   - `post_count`
5. Extract representative viewpoints:
   - prioritize concrete opinions, catalysts, concerns, valuation views, trading interpretations
   - avoid repetitive phrasing and low-information remarks

### 4. Aggregate Analysis

If only **1 symbol**:

- output that symbol's sentiment result directly
- generate one-line summary
- extract top `3` viewpoints for that symbol

If **multiple symbols**:

1. Compute **group-level sentiment** across all retained posts from all symbols.
2. Generate one-line **group summary**.
3. Identify whether group sentiment is driven by one or several symbols.
4. Then provide **per-symbol breakdown**.
5. Extract top `3` group-level viewpoints across the combined sample.

### 5. Organize the Information

The response should always include:

1. a headline with target/group name
2. sentiment percentages
3. total retained post count
4. a concise summary sentence
5. top viewpoints
6. disclaimer

### 6. Return Structured Result

Return a normalized object so downstream callers can reliably parse the result.

### 7. Append Disclaimer

Every user-facing answer must end with a non-investment disclaimer.

### 8. Platform Source Footer

When both `moomoo-comment-sentiment` and `futu-comment-sentiment` are installed, append a platform source line after the disclaimer, matching the user's language:

- English: `Source: moomoo | English queries default to moomoo; Chinese queries default to Futu. Say "use futu" to switch.`
- Chinese: `数据来源：moomoo | 英文默认使用 moomoo，中文默认使用牛牛。输入「用牛牛查」可切换平台。`

If only this skill is installed (no Futu counterpart), do not show the platform source footer.

---

## Retrieval Parameters

### Required Logical Inputs

- `symbol_list`: array of one or more targets

### Optional Logical Inputs

- `group_name`: optional portfolio or group label
- `lang`: optional language hint
- `size_per_symbol`: optional retrieval count per symbol when the upstream API requires an explicit size; default `30`, clamp to `1-50`

### Validation Rules

| Check | Rule |
| ----- | ---- |
| `symbol_list` missing or empty | Reject and ask for at least one symbol. |
| empty symbol after trim | Drop it and note it internally. |
| duplicate symbols | Deduplicate while preserving original order. |
| `size_per_symbol` omitted | Default to `30`. |
| `size_per_symbol < 1` | Clamp to `1`. |
| `size_per_symbol > 50` | Clamp to `50` unless deployment allows more. |

---

## Upstream Data Contract

This skill assumes an upstream moomoo discussion/feed endpoint similar to `stock_feed` or a community feed search endpoint that can retrieve recent stock-related posts.

Typical request shape:

```bash
curl -sG 'https://ai-news-search.moomoo.com/stock_feed' \
  -H 'User-Agent: moomoo-comment-sentiment/0.0.2 (Skill)' \
  --data-urlencode 'keyword=NVDA' \
  --data-urlencode 'size=30'
```

Common top-level response:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `code` | int32 | `0` means success |
| `message` | string | error message or empty string |
| `data` | array | list of feed/community items |

Common item fields:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | unique post ID |
| `title` | string | post title |
| `desc` | string | post content or excerpt, may contain HTML |
| `publish_time` | string \| int64 | publish timestamp |
| `url` | string | optional deep link |

If the actual upstream endpoint exposes extra fields such as interaction count, likes, comments, or heat score, the agent should use them to improve low-quality filtering.

---

## Sentiment Classification Rules

Use only three labels at the **post level**:

- `bullish`
- `bearish`
- `neutral`

Use four labels at the **aggregate level** when needed:

- `bullish`
- `bearish`
- `neutral`
- `mixed`

### Bullish Cues

Examples:

- expectation of rise, rebound, breakout, upside
- confidence in earnings, product cycle, AI demand, orders, margin expansion
- supportive valuation discussion
- optimistic dip-buying or long-term holding rationale

### Bearish Cues

Examples:

- expectation of drop, retracement, weak outlook, demand softness
- concern about earnings miss, competition, regulation, dilution, delivery issues
- negative valuation view
- panic, capitulation, or strongly risk-off tone

### Neutral Cues

Examples:

- factual updates without directional opinion
- watch-and-see commentary
- mixed or ambiguous stance
- low-confidence content with no clear directional bias

### Mixed Aggregate Rule

If bullish and bearish shares are both meaningful and neither side has a clear edge, the aggregate result may use `mixed`.

Recommended rule:

- if `abs(bull_pct - bear_pct) < 15%`
- and both `bull_pct >= 25%` and `bear_pct >= 25%`
- aggregate label may be `mixed`

Otherwise:

- dominant bullish share -> `bullish`
- dominant bearish share -> `bearish`
- weak directional evidence -> `neutral`

---

## Low-Quality Filtering Rules

This step is mandatory. Do not treat every retrieved post equally.

### Filter Out Or Down-Weight

- extremely short filler content such as only emojis, only "to the moon", only "nice", only ticker repeats
- pure repost markers with no view
- obvious spam, ads, referral text, or off-topic content
- repetitive slogan-style content with no incremental information
- machine-like templated posts
- posts with extremely weak interaction when interaction signals are available

### Keep Preferentially

- posts with explicit directional view
- posts with concrete reasons, catalysts, or concerns
- posts with clear disagreement that explains why the market is split
- posts with meaningful interaction or recognizable discussion value

### Important Guardrail

If interaction fields are **not** available upstream, still perform text-quality filtering. Do not fabricate interaction-based thresholds.

---

## Group-Level Aggregation Rules

When multiple symbols are provided, follow this exact order:

1. complete per-symbol filtering and sentiment counting first
2. merge all retained posts across symbols into one combined sample
3. compute:
   - `group_bull_pct`
   - `group_bear_pct`
   - `group_neutral_pct`
   - `group_post_count`
4. generate one-line `group_summary`
5. identify which symbols contribute most to the current group tone
6. output per-symbol breakdown after the overall result

### Group Summary Style

Good examples:

- `Overall sentiment is bullish, with optimism driven mainly by NVDA while TSLA remains more divided.`
- `Portfolio sentiment is broadly neutral to cautious, with bearish views focused on demand and valuation pressure.`
- `The overall sample shows clear disagreement, with AAPL more stable while TSLA and NVDA are more polarized.`

Avoid:

- fake precision unsupported by the data
- strong causal claims about future price
- investment recommendations

---

## Hot Opinion Extraction Rules

Extract **Top 3** viewpoints from retained posts.

Requirements:

1. Use short user-style opinion summaries, preferably quotable.
2. Merge duplicate or near-duplicate opinions before ranking.
3. Prefer viewpoints that are:
   - repeated across multiple posts
   - specific and interpretable
   - representative of current mood
4. Avoid generic filler such as:
   - "still watching"
   - "let's wait and see"
   - "big move today"
5. Sort the final top opinions by `published_at` descending (most recent first).

In multi-symbol mode:

- extract top `3` **group-level** opinions first
- optionally mention the driving symbol inside the summary if needed

---

## User-Facing Output Templates

### Single Symbol Template

```markdown
{{symbol}} Community Sentiment · Real Time
Data window: {{time_range_earliest}} ~ {{time_range_latest}}

Community:
Bullish {{bull_pct}}% · Bearish {{bear_pct}}% · Neutral {{neutral_pct}}%
(Based on {{post_count}} posts)

Summary:
{{summary}}

Top viewpoints:

1. "{{opinion_1}}" · {{opinion_1_time}}
2. "{{opinion_2}}" · {{opinion_2_time}}
3. "{{opinion_3}}" · {{opinion_3_time}}

This content is compiled from public information and does not constitute investment advice.

{{platform_source_footer}}
```

### Multi-Symbol Template

```markdown
{{group_name}} Community Sentiment · Real Time
Data window: {{time_range_earliest}} ~ {{time_range_latest}}

Overall community:
Bullish {{group_bull_pct}}% · Bearish {{group_bear_pct}}% · Neutral {{group_neutral_pct}}%
(Based on {{group_post_count}} posts)

Overall summary:
{{group_summary}}

Per-symbol sentiment:

- {{symbol_1}}: Bullish {{bull_pct_1}}% · Bearish {{bear_pct_1}}% · Neutral {{neutral_pct_1}}%
- {{symbol_2}}: Bullish {{bull_pct_2}}% · Bearish {{bear_pct_2}}% · Neutral {{neutral_pct_2}}%
- {{symbol_3}}: Bullish {{bull_pct_3}}% · Bearish {{bear_pct_3}}% · Neutral {{neutral_pct_3}}%

Top viewpoints:

1. "{{opinion_1}}" · {{opinion_1_time}}
2. "{{opinion_2}}" · {{opinion_2_time}}
3. "{{opinion_3}}" · {{opinion_3_time}}

This content is compiled from public information and does not constitute investment advice.

{{platform_source_footer}}
```

### Display Rules

1. If only one symbol is supplied, do not show group-level wrapper fields.
2. If fewer than `3` valid opinions exist, show only the actual number available.
3. If one symbol has too little valid data after filtering, explicitly say evidence is limited.
4. Never expose raw upstream IDs in normal user-facing output.
5. For English output, use `Bullish / Bearish / Neutral / Mixed` consistently in labels and summaries.
6. Timestamp display format for `published_at` on opinions: `MM-DD HH:mm` (e.g., `04-01 19:45`). Omit the date part if all opinions are from today relative to `generated_at`.
7. The `Data window` header range uses `MM-DD HH:mm` on both ends. If earliest and latest are on the same calendar day, the format may be shortened to `HH:mm ~ HH:mm` with the date shown once.

---

## Normalized Output Contract

Return one structured object with the following top-level fields:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `request` | object | effective request parameters |
| `generated_at` | string | ISO-8601 completion timestamp |
| `mode` | string | `single` or `multi` |
| `group` | object \| null | overall portfolio sentiment when `mode=multi` |
| `symbols` | array | per-symbol sentiment results |
| `top_opinions` | Opinion[] | top 3 overall opinions for user display |
| `disclaimer` | string | fixed disclaimer |

### `Opinion`

| Field | Type | Description |
| ----- | ---- | ----------- |
| `text` | string | opinion summary text |
| `published_at` | string | human-readable time string, `YYYY-MM-DD HH:mm` (UTC+8) |

### `request`

| Field | Type |
| ----- | ---- |
| `symbol_list` | string[] |
| `group_name` | string \| null |
| `lang` | string \| null |
| `size_per_symbol` | int32 |

### `group`

Only required when `mode=multi`.

| Field | Type | Description |
| ----- | ---- | ----------- |
| `label` | string | `bullish` / `bearish` / `neutral` / `mixed` |
| `bull_pct` | string | percentage string |
| `bear_pct` | string | percentage string |
| `neutral_pct` | string | percentage string |
| `post_count` | int32 | retained group post count |
| `summary` | string | one-line group summary |

### `symbols[]`

| Field | Type | Description |
| ----- | ---- | ----------- |
| `symbol` | string | target symbol |
| `status` | string | `ok` / `error` / `empty` |
| `upstream_code` | int32 | raw upstream status |
| `upstream_message` | string | raw upstream message |
| `label` | string | `bullish` / `bearish` / `neutral` / `mixed` |
| `bull_pct` | string | percentage string |
| `bear_pct` | string | percentage string |
| `neutral_pct` | string | percentage string |
| `post_count` | int32 | retained post count |
| `time_range` | object | `{ earliest: string, latest: string }` in `YYYY-MM-DD HH:mm` (UTC+8), derived from the full pre-filter batch |
| `summary` | string | one-line symbol summary |
| `top_opinions` | Opinion[] | top viewpoints for this symbol, each with `text` and `published_at` |
| `signals` | object | optional reasoning evidence |

### `symbols[].signals`

| Field | Type | Description |
| ----- | ---- | ----------- |
| `bullish_signals` | string[] | repeated positive cues |
| `bearish_signals` | string[] | repeated negative cues |
| `uncertainties` | string[] | weak evidence or ambiguity |

---

## Minimal JSON Example

```json
{
  "request": {
    "symbol_list": ["NVDA", "TSLA", "AAPL"],
    "group_name": "US Tech Portfolio",
    "lang": "en",
    "size_per_symbol": 30
  },
  "generated_at": "2026-04-01T10:00:00.000Z",
  "mode": "multi",
  "group": {
    "label": "bullish",
    "bull_pct": "61%",
    "bear_pct": "27%",
    "neutral_pct": "12%",
    "post_count": 842,
    "summary": "Overall sentiment is bullish, with optimism driven mainly by NVDA while TSLA remains more divided."
  },
  "symbols": [
    {
      "symbol": "NVDA",
      "status": "ok",
      "upstream_code": 0,
      "upstream_message": "",
      "label": "bullish",
      "bull_pct": "68%",
      "bear_pct": "22%",
      "neutral_pct": "10%",
      "post_count": 286,
      "time_range": { "earliest": "2026-04-01 17:32", "latest": "2026-04-01 19:57" },
      "summary": "Community sentiment is broadly bullish, with optimism centered on AI demand and earnings follow-through.",
      "top_opinions": [
        { "text": "AI demand is still accelerating, and NVDA's run may not be over", "published_at": "2026-04-01 19:45" },
        { "text": "The pullback looks more like trading noise than a change in the medium-term thesis", "published_at": "2026-04-01 18:51" },
        { "text": "Valuation is not cheap, but the fundamentals are still delivering", "published_at": "2026-04-01 18:03" }
      ],
      "signals": {
        "bullish_signals": ["AI demand", "earnings momentum"],
        "bearish_signals": ["valuation concern"],
        "uncertainties": ["short-term momentum can reverse quickly"]
      }
    },
    {
      "symbol": "TSLA",
      "status": "ok",
      "upstream_code": 0,
      "upstream_message": "",
      "label": "mixed",
      "bull_pct": "49%",
      "bear_pct": "38%",
      "neutral_pct": "13%",
      "post_count": 301,
      "time_range": { "earliest": "2026-04-01 16:10", "latest": "2026-04-01 19:55" },
      "summary": "Bullish and bearish views are clearly split, with optimism coexisting alongside demand concerns.",
      "top_opinions": [
        { "text": "This TSLA move feels more like a sentiment rebound than a solid reset", "published_at": "2026-04-01 19:30" },
        { "text": "The new narrative is still alive, but delivery pressure has not gone away", "published_at": "2026-04-01 18:22" },
        { "text": "If deliveries improve, sentiment could recover quickly", "published_at": "2026-04-01 17:48" }
      ],
      "signals": {
        "bullish_signals": ["narrative rebound"],
        "bearish_signals": ["delivery pressure", "demand concern"],
        "uncertainties": ["opinion split is large"]
      }
    }
  ],
  "top_opinions": [
    { "text": "AI demand is still accelerating, and NVDA's run may not be over", "published_at": "2026-04-01 19:45" },
    { "text": "This TSLA move feels more like a sentiment rebound than a solid reset", "published_at": "2026-04-01 19:30" },
    { "text": "Apple has limited near-term upside and looks more like a defensive allocation", "published_at": "2026-04-01 18:10" }
  ],
  "disclaimer": "This content is compiled from public information and does not constitute investment advice."
}
```

---

## Behavior Rules

1. Always parse the request into `symbol_list` first. Do not reduce a portfolio request into a single-keyword task.
2. Always apply low-quality filtering before computing percentages.
3. Base conclusions on retrieved discussion text, not prior market knowledge.
4. If upstream fails for one symbol, keep the batch result and mark that symbol as failed.
5. If a symbol has too few valid posts after filtering, say evidence is limited instead of over-interpreting.
6. In multi-symbol mode, output the **group result first**, then per-symbol breakdown.
7. Hot opinions should be de-duplicated summaries, not raw copied spam.
8. Never provide buy/sell advice or imply certain future price direction.

---

## Authentication

- Public gateway usage typically does not require explicit API keys in the documented contract.
- If an internal deployment later adds authentication, use environment variables or secret storage and never hardcode secrets in this skill.

---

## Security

### Requests And Data

- Treat all symbols as user input and URL-encode them.
- Strip HTML before display.
- Avoid logging large raw post bodies when not needed.
- Do not expose internal gateway details, cookies, or secrets.

### Disclaimer

- Community sentiment is only a discussion-sample summary.
- Sentiment does not equal future price direction.
- Responses are informational only and not investment advice.

---

## User Agent Header

Include a `User-Agent` header with the following string: `moomoo-comment-sentiment/0.0.2 (Skill)`

## moomoo-capital-anomaly

---
name: moomoo-capital-anomaly
description: >-
  Detects capital-flow anomaly signals for a user-mentioned stock with
  `get_financial_unusual`, including 资金分布、买卖经纪商、资金流向、卖空数量、
  卖空比例 and their unusual changes. Use when the user asks about 资金动向、资金异动、
  净流入、净流出、主力行为、大单小单、谁在买谁在卖、买卖经纪商、卖空异动、
  卖空/做空/沽空、主力是否在进场或离场，or gives a
  broad stock-anomaly request such as “英伟达异动”、“NVDA 异动”、“腾讯有没有异动/异常”
  without narrowing the dimension. For broad anomaly requests, this skill should
  be used together with `technical-anomaly` and `derivatives-anomaly`. Before
  calling the script, you must first normalize the user-mentioned stock name,
  Chinese company name, English company name, or ticker into a standard symbol
  such as `US.TSLA` or `HK.00700`.
metadata:
  version: 0.0.1
  author: Futu
license: MIT
---

# Capital Anomaly Skill

Detects capital-flow anomalies for a specific stock and formats the result as a structured capital anomaly summary.

This skill is for **异动检测** rather than a regular capital-flow overview. If the data has no qualifying anomaly, return `无异常` or the interface's no-data result, and do not add extra market commentary.

If the user only says a broad request such as `英伟达异动`、`NVDA 异动`、`腾讯有没有异常` and does not specify a dimension, treat it as a bundled anomaly request. In that case, this skill should be used as one of the three default anomaly skills together with `technical-anomaly` and `derivatives-anomaly`.

---

## Workflow

### 1. Parse User Input

Extract the following from the user's request:

- `stock_target`: stock code, Chinese stock name, English company name, or ticker explicitly mentioned by the user
- `time_range`: default `7`; if the user says "最近 3 天" / "过去两周" / "last 5 days", convert it to a natural-day integer
- `analysis_dimensions`: optional; only extract when the user clearly asks about one or more specific financial dimensions
- `language_id`: infer from the user's language

If the target stock is missing, ask a follow-up question instead of guessing.

### 2. Normalize the Stock Target into a Standard Symbol

Before calling the script, convert the user-mentioned stock target into a standard symbol such as `US.TSLA`, `HK.00700`, `SH.600519`, or `SZ.000001`.

Normalization rules:

- If the user already gives a fully qualified symbol like `US.TSLA` or `HK.00700`, use it directly.
- If the user gives a Chinese company name, English company name, or common ticker, map it to the matching market-prefixed symbol.
- If the symbol is ambiguous, ask a follow-up question instead of guessing.

Common mappings:

| User mention | Standard symbol |
|--------------|-----------------|
| 腾讯 | `HK.00700` |
| 阿里巴巴、阿里 | `HK.09988` |
| 苹果、Apple | `US.AAPL` |
| 特斯拉、Tesla | `US.TSLA` |
| 英伟达、NVIDIA | `US.NVDA` |
| 微软、Microsoft | `US.MSFT` |
| 谷歌、Google、Alphabet | `US.GOOG` |
| 亚马逊、Amazon | `US.AMZN` |
| Meta、脸书、Facebook | `US.META` |
| 台积电、TSM | `US.TSM` |
| 贵州茅台、茅台 | `SH.600519` |
| 宁德时代 | `SZ.300750` |

Ticker inference guidance:

- `TSLA`, `AAPL`, `NVDA`, `MSFT`, `GOOG`, `META` usually mean US stocks, so normalize to `US.TSLA`, `US.AAPL`, `US.NVDA`, `US.MSFT`, `US.GOOG`, `US.META`.
- `00700` by itself is ambiguous in plain text; when the context clearly refers to Tencent, normalize to `HK.00700`.
- If the same company has both HK and US listings and the user does not specify the market, ask a clarifying question.

### 3. Map Financial Intent to `analysis_dimensions`

Prefer these canonical `analysis_dimensions` values:

- `funds_distribution`: 资金分布
- `funds_broker`: 买卖经纪商
- `funds_flow`: 资金流向
- `short_sell_number`: 卖空数量
- `short_sell_ratio`: 卖空比例
- `short_sell_number_and_ratio`: 卖空数量和比例同时异动

Selection guidance:

- If the user asks about `谁在买/谁在卖/经纪商`, include `funds_broker`.
- If the user asks about `大单小单/资金分歧/资金分布`, include `funds_distribution`.
- If the user asks about `主力连续流入流出/资金流向`, include `funds_flow`.
- If the user asks about `卖空数量`, include `short_sell_number`.
- If the user asks about `卖空比例`, include `short_sell_ratio`.
- If the user asks about `卖空数量和比例是否同时异常`, include `short_sell_number_and_ratio`.
- If the user asks a broad 资金面问题 and does not narrow scope, omit `analysis_dimensions` and use the full interface.

### 4. Infer `language_id`

Use the following language mapping:

- `0`: 简中
- `1`: 繁中
- `2`: 英文
- `4`: 泰语
- `5`: 日语

Default strategy:

- Chinese user -> `0`
- Traditional Chinese request -> `1`
- English user -> `2`
- If unclear, default to `0`

### 5. Call the Script

After extracting and normalizing the parameters, call the script with a Python 3 interpreter. Prefer `python3`; only fall back to `python` when `python3` is unavailable. This avoids the common macOS case where `python` is not installed or not on `PATH`.

Script entry:

```bash
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_capital_anomaly.py <STANDARD_SYMBOL> --time-range <DAYS> [--analysis-dimensions ...] [--language-id <ID>] --json
```

Examples:

```bash
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_capital_anomaly.py US.NVDA --time-range 7 --json
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_capital_anomaly.py HK.00700 --time-range 7 --analysis-dimensions funds_distribution funds_broker --json
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_capital_anomaly.py US.AAPL --time-range 5 --analysis-dimensions funds_flow --json
```

### 6. Check the Result

- If the script exits successfully, use the returned data to build a structured capital-flow anomaly summary.
- If the script returns an error, surface the error message and do not fabricate results.
- If a requested class has no anomaly in the window, explicitly say `无异常`.
- If the downstream service reports a permission problem or no accessible data, clearly state that the stock or account lacks the required permission.

---

## Parameters

### Required

- `stock_symbol`: standard market-prefixed symbol, such as `US.TSLA`, `HK.00700`, `SH.600519`, `SZ.000001`

### Optional

- `time_range`: natural day window, default `7`
- `analysis_dimensions`: list of specific financial anomaly dimensions to inspect; omit for full scan
- `language_id`: output language, default `0`

---

## Output Rules

Present the output by anomaly class. The three high-level classes are:

- `资金分布与买卖经纪商`
- `资金流向`
- `卖空情况`

Formatting rules:

- Always display `时间范围` as an absolute date range in the format `YYYY.M.D - YYYY.M.D`. Calculate the start date from the current date minus `time_range` days (e.g., if today is 2026.4.24 and time_range is 7, write `时间范围：2026.4.18 - 2026.4.24`).
- If multiple abnormal dates appear within the window for one class, list them all.
- If a class has no anomaly in the window, write `无异常`.
- Preserve dates, direction, amount, ratio, broker names, and interpretation from the tool output.
- Do not merge different anomaly classes into one sentence.
- Do not invent thresholds, rankings, or causal explanations beyond the returned content.
- If the user only asked about a subset of financial dimensions, keep only the relevant classes.

---

## Preferred Response Template

```markdown
时间范围：{YYYY.M.D - YYYY.M.D}

- 资金分布与买卖经纪商：{异常内容或“无异常”}
- 资金流向：{异常内容或“无异常”}
- 卖空情况：{异常内容或“无异常”}
```

When the user only asks for a subset, keep only the relevant classes.

---

## Behavior Rules

1. Always normalize the user-mentioned stock target into a standard symbol before calling the script.
2. If the target stock is missing, ask a follow-up question.
3. If the market is ambiguous, ask a follow-up question instead of guessing.
4. If the user asks a broad 资金面问题, omit `analysis_dimensions` and use the full interface.
5. Do not output raw JSON by default when talking to the user, even if the script returns JSON.
6. Do not interpret the result as investment advice or trading guidance.
7. If the downstream service reports a permission issue, state that clearly and do not fabricate analysis.

---

## Example User Requests

### Broad capital anomaly check

- "特斯拉最近 7 天有没有资金面异动？"
- "看看腾讯最近主力有没有异常动作"
- "帮我查一下 Apple 最近资金面有没有异常"

Mapped request:

```json
{
  "stock_symbol": "US.TSLA",
  "time_range": 7,
  "language_id": 0
}
```

### Broker and capital-distribution only

- "腾讯最近谁在买谁在卖？"
- "00700 最近大单小单有没有分歧？"

Mapped request:

```json
{
  "stock_symbol": "HK.00700",
  "time_range": 7,
  "analysis_dimensions": ["funds_distribution", "funds_broker"],
  "language_id": 0
}
```

### Funds flow only

- "苹果最近主力资金有连续流入流出吗？"

Mapped request:

```json
{
  "stock_symbol": "US.AAPL",
  "time_range": 5,
  "analysis_dimensions": ["funds_flow"],
  "language_id": 0
}
```

### Short sell only

- "TSLA 最近卖空比例有没有异常？"

Mapped request:

```json
{
  "stock_symbol": "US.TSLA",
  "time_range": 7,
  "analysis_dimensions": ["short_sell_ratio"],
  "language_id": 0
}
```

---

## Example Interpretation Style

```markdown
时间范围：2026.4.2 - 2026.4.9

- 资金分布与买卖经纪商：4.3，特大单净流入1.13亿元且流入流出金额相差一倍以上，小单净流出1.78亿元，方向相反，代表大资金和小资金存在分歧；从买卖经纪商看，买入排名前二的是中国投资（沪港通）和富途证券，卖出排名前二的是瑞银和巴克莱亚洲。
- 资金流向：4.4，主力资金近4日持续净流出，当日净流出金额比前3日均值高120%，表明主力资金在加速离场。
- 卖空情况：4.5，卖空数量和卖空比例同时异动，卖空数量日环比上升，卖空比例也同步抬升，且两者均高于近一月均值，体现较强烈的看空预期。
```

## moomoo-derivatives-anomaly

---
name: moomoo-derivatives-anomaly
description: >-
  Detects derivatives anomaly signals for a user-mentioned stock with
  `get_derivative_unusual`, including 牛熊证街货比例、异动、anomaly, 牛熊证街货价格区间、期权大单、
  隐含波动率、期权量价、期权情绪、期权综合信号 and their unusual changes. Use
  when the user asks about 期权、衍生品、牛熊证、IV、隐含波动率、PCR、期权大单、
  期权异常成交、聪明钱、smart money、unusual options activity、做多做空情绪、
  波动率溢价、期权市场怎么看、有没有大单押注、大资金押注、适不适合卖期权，or gives a
  broad stock-anomaly request such as “英伟达异动”、“NVDA 异动”、“腾讯有没有异动/异常”
  without narrowing the dimension. For broad anomaly requests, this skill should
  be used together with `technical-anomaly` and `capital-anomaly`. Before
  calling the script, you must first normalize the user-mentioned stock name,
  Chinese company name, English company name, or ticker into a standard symbol
  such as `US.NVDA` or `HK.00700`.
metadata:
  version: 0.0.1
  author: Futu
license: MIT
---

# Derivatives Anomaly Skill

Detects derivatives anomalies for a specific stock and formats the result as a structured derivatives anomaly summary.

This skill is for **异动检测** rather than a regular derivatives overview. If the data has no qualifying anomaly, return `无异常` or `无异常（简要原因）`, and do not add extra market commentary.

If the user only says a broad request such as `英伟达异动`、`NVDA 异动`、`腾讯有没有异常` and does not specify a dimension, treat it as a bundled anomaly request. In that case, this skill should be used as one of the three default anomaly skills together with `technical-anomaly` and `capital-anomaly`.

---

## Workflow

### 1. Parse User Input

Extract the following from the user's request:

- `stock_target`: stock code, Chinese stock name, English company name, or ticker explicitly mentioned by the user
- `time_range`: default `7`; if the user says "最近 3 天" / "过去两周" / "last 5 days", convert it to a natural-day integer
- `analysis_dimensions`: optional; only extract when the user clearly asks about one or more specific derivatives dimensions
- `language_id`: infer from the user's language

If the target stock is missing, ask a follow-up question instead of guessing.

### 2. Normalize the Stock Target into a Standard Symbol

Before calling the script, convert the user-mentioned stock target into a standard symbol such as `US.NVDA`, `HK.00700`, `SH.600519`, or `SZ.000001`.

Normalization rules:

- If the user already gives a fully qualified symbol like `US.NVDA` or `HK.00700`, use it directly.
- If the user gives a Chinese company name, English company name, or common ticker, map it to the matching market-prefixed symbol.
- If the symbol is ambiguous, ask a follow-up question instead of guessing.

Common mappings:

| User mention | Standard symbol |
|--------------|-----------------|
| 腾讯 | `HK.00700` |
| 阿里巴巴、阿里 | `HK.09988` |
| 苹果、Apple | `US.AAPL` |
| 特斯拉、Tesla | `US.TSLA` |
| 英伟达、NVIDIA | `US.NVDA` |
| 微软、Microsoft | `US.MSFT` |
| 谷歌、Google、Alphabet | `US.GOOG` |
| 亚马逊、Amazon | `US.AMZN` |
| Meta、脸书、Facebook | `US.META` |
| 台积电、TSM | `US.TSM` |
| 贵州茅台、茅台 | `SH.600519` |
| 宁德时代 | `SZ.300750` |

Ticker inference guidance:

- `NVDA`, `AAPL`, `TSLA`, `MSFT`, `GOOG`, `META` usually mean US stocks, so normalize to `US.NVDA`, `US.AAPL`, `US.TSLA`, `US.MSFT`, `US.GOOG`, `US.META`.
- `00700` by itself is ambiguous in plain text; when the context clearly refers to Tencent, normalize to `HK.00700`.
- If the same company has both HK and US listings and the user does not specify the market, ask a clarifying question.

### 3. Map Derivatives Intent to `analysis_dimensions`

Prefer these canonical `analysis_dimensions` values:

- `warrant_ratio`: 牛熊证街货比例异动，仅港股
- `warrant_price_distribution`: 牛熊证街货价格区间异动，仅港股
- `option_unusual`: 期权大单异动
- `option_volatility`: 期权波动率异动
- `option_volume_price`: 期权量价异动
- `option_sentiment`: 期权情绪异动
- `option_comprehensive`: 期权综合信号异动

Selection guidance:

- If the user asks about `牛熊证街货比例/牛熊街货比例`, include `warrant_ratio`.
- If the user asks about `重货区/街货价格区间/支撑压力`, include `warrant_price_distribution`.
- If the user asks about `期权大单/大额成交/V/OI/聪明钱押注`, include `option_unusual`.
- If the user asks about `IV/IV percentile/IV rank/HV/波动率溢价`, include `option_volatility`.
- If the user asks about `成交量/持仓量/OI/正股联动`, include `option_volume_price`.
- If the user asks about `PCR/Put Call Ratio/做多做空情绪`, include `option_sentiment`.
- If the user asks about `综合信号/多维背离`, include `option_comprehensive`.
- If the user asks a broad 衍生品问题 and does not narrow scope, omit `analysis_dimensions` and use the full interface.

### 4. Infer `language_id`

Use the following language mapping:

- `0`: 简中
- `1`: 繁中
- `2`: 英文
- `4`: 泰语
- `5`: 日语

Default strategy:

- Chinese user -> `0`
- Traditional Chinese request -> `1`
- English user -> `2`
- If unclear, default to `0`

### 5. Call the Script

After extracting and normalizing the parameters, call the script with a Python 3 interpreter. Prefer `python3`; only fall back to `python` when `python3` is unavailable. This avoids the common macOS case where `python` is not installed or not on `PATH`.

Script entry:

```bash
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_derivatives_anomaly.py <STANDARD_SYMBOL> --time-range <DAYS> [--analysis-dimensions ...] [--language-id <ID>] --json
```

Examples:

```bash
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_derivatives_anomaly.py HK.00700 --time-range 7 --json
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_derivatives_anomaly.py US.NVDA --time-range 7 --analysis-dimensions option_unusual option_volatility --json
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_derivatives_anomaly.py US.AAPL --time-range 7 --analysis-dimensions option_sentiment option_comprehensive --json
```

### 6. Check the Result

- If the script exits successfully, use the returned data to build a structured derivatives anomaly summary.
- If the script returns an error, surface the error message and do not fabricate results.
- If a requested class has no anomaly in the window, explicitly say `无异常` or `无异常（简要原因）`.
- If the downstream service reports a permission problem or no accessible data, clearly state that the stock or account lacks the required permission.
- If the stock is not Hong Kong listed, warrant-related classes should be marked as `不适用` or `无异常`.

---

## Parameters

### Required

- `stock_symbol`: standard market-prefixed symbol, such as `US.NVDA`, `HK.00700`, `SH.600519`, `SZ.000001`

### Optional

- `time_range`: natural day window, default `7`
- `analysis_dimensions`: list of specific derivatives anomaly dimensions to inspect; omit for full scan
- `language_id`: output language, default `0`

---

## Output Rules

Present the output by anomaly class. The seven classes are:

- `牛熊证街货比例异动（港股）`
- `牛熊证街货价格区间异动（港股）`
- `期权大单异动`
- `期权波动率异动`
- `期权量价异动`
- `期权情绪异动`
- `期权综合信号异动`

Formatting rules:

- Always display `时间范围` as an absolute date range in the format `YYYY.M.D - YYYY.M.D`. Calculate the start date from the current date minus `time_range` days (e.g., if today is 2026.4.24 and time_range is 7, write `时间范围：2026.4.18 - 2026.4.24`).
- Always preserve the class order above.
- **Full scan** (no `analysis_dimensions` specified): always show all 7 class names. Write `无异常` for classes with no anomaly. Never omit a class name.
- **Subset request** (user specifies one or more dimensions): show only the classes that correspond to the requested dimensions. Write `无异常` for requested classes that have no anomaly. Do not show unrelated classes.
- If multiple abnormal dates or timestamps appear within one class, list them all.
- For `期权大单异动`, when multiple unusual option trades exist in the window, show all of them. Do not collapse them to only the highest-premium trade.
- Keep dates, timestamps, direction, volume, open interest, `V/OI`, premium amount, strike, expiry, percentile, price zone, and interpretation from the tool output.
- Do not merge different anomaly classes into one sentence.
- Warrant-related classes (`牛熊证街货比例异动（港股）` and `牛熊证街货价格区间异动（港股）`) apply to Hong Kong stocks only. If the stock is not Hong Kong listed, **omit these two classes entirely** from the output. Do not show them with `不适用`.
- Do not invent thresholds, rankings, or causal explanations beyond the returned content.

---

## Preferred Response Template

```markdown
时间范围：{YYYY.M.D - YYYY.M.D}

牛熊证街货比例异动（港股）：
{异常内容或“无异常”}

牛熊证街货价格区间异动（港股）：
{异常内容或“无异常”}

期权大单异动：
{逐条列出全部异常，或“无异常”}

期权波动率异动：
{异常内容或“无异常”}

期权量价异动：
{异常内容或“无异常”}

期权情绪异动：
{异常内容或“无异常”}

期权综合信号异动：
{异常内容或“无异常”}
```

When the user only asks for a subset, keep only the relevant classes.

---

## Behavior Rules

1. Always normalize the user-mentioned stock target into a standard symbol before calling the script.
2. If the target stock is missing, ask a follow-up question.
3. If the market is ambiguous, ask a follow-up question instead of guessing.
4. If the user asks a broad 衍生品问题, omit `analysis_dimensions` and use the full interface.
5. Do not output raw JSON by default when talking to the user, even if the script returns JSON.
6. Do not interpret the result as investment advice or trading guidance.
7. If the downstream service reports a permission issue, state that clearly and do not fabricate analysis.
8. For non-HK stocks, do not force warrant-specific conclusions; use `不适用` or `无异常`.

---

## Example User Requests

### Broad derivatives anomaly check

- "腾讯最近 7 天有没有衍生品异动？"
- "看看 NVDA 最近期权市场有没有异常"
- "帮我查一下 Apple 最近衍生品有没有异动"

Mapped request:

```json
{
  "stock_symbol": "HK.00700",
  "time_range": 7,
  "language_id": 0
}
```

### IV and sentiment only

- "AAPL 最近 IV 和期权情绪有没有异常？"
- "苹果最近期权波动率和 PCR 怎么样？"

Mapped request:

```json
{
  "stock_symbol": "US.AAPL",
  "time_range": 7,
  "analysis_dimensions": ["option_volatility", "option_sentiment"],
  "language_id": 0
}
```

### Unusual option trades only

- "NVDA 最近有没有期权大单押注？"
- "英伟达最近有没有异常期权成交？"

Mapped request:

```json
{
  "stock_symbol": "US.NVDA",
  "time_range": 7,
  "analysis_dimensions": ["option_unusual"],
  "language_id": 0
}
```

### Warrant-related only

- "腾讯最近牛熊证街货比例有没有异常？"
- "00700 最近重货区在哪里？"

Mapped request:

```json
{
  "stock_symbol": "HK.00700",
  "time_range": 7,
  "analysis_dimensions": ["warrant_ratio", "warrant_price_distribution"],
  "language_id": 0
}
```

---

## Example Interpretation Style

```markdown
时间范围：2026.4.2 - 2026.4.9

牛熊证街货比例异动（港股）：
4.3，牛证街货的占比达到82.2%，高于近一年90%的交易日，说明更多投资者持有牛证过夜，反映出看多情绪。
4.7，熊证街货的占比达到17.8%，高于近一年90%的交易日，说明更多投资者持有熊证过夜，反映出看空情绪。

牛熊证街货价格区间异动（港股）：
4.3，牛证的重货区位于95.0-100.0回收价区间，接近当日收市价，说明有较多投资者持有该价格区间的牛证，反映较多投资者认为该价位形成支撑位。
4.7，牛证的最多新增与重货区同时位于95.0-100.0回收价区间，说明较多投资者新增持有了该价格区间的牛证，反映较多投资者认为该价位形成支撑位。

期权大单异动：
4.4 15:31，产生了一笔看涨期权大单，成交量达到1000张，远超过未平仓数130张，V/OI值高达15.2，通常暗示有交易者在新建数量异常的头寸，该交易涉资7.5万美元，合约行权价是10美元，到期日为2025/09/08。
4.6 10:15，产生了一笔看跌期权大单，成交量达到800张，远超过未平仓数50张，V/OI值高达16.0，该交易涉资5.2万美元，合约行权价是165美元，到期日为2025/05/02。

期权波动率异动：
4.5，隐含波动率(IV)处于历史高位，且显著高于已实现的历史波动率(HV)，存在IV-HV值的高额溢价。此环境对期权卖方有利，可卖出期权博弈波动率的均值回归。
4.7，隐含波动率(IV)百分位数达到95，说明隐含波动率超越近一年的大多数日期，时间价值高，可以使用期权卖出策略。

期权量价异动：
4.5，期权成交量环比增长52%，持仓量环比增长48%，正股价格上涨3.5%，可能是做多资金在大量进场，未来上涨趋势可能继续。期权市场整体在260附近出现显著的成交和持仓集中现象，该价位可能成为重要的支撑或阻力位。

期权情绪异动：
4.3，期权Put/Call Ratio百分位达到89，高于近一年89%的交易日，且连续2日上升，看跌期权活跃度显著增加。

期权综合信号异动：
4.8，正股近期出现较大跌幅，但期权隐含波动率百分位变化不大，市场并未出现恐慌性定价，历史上类似情形后常孕育反弹机会。
```

## moomoo-technical-anomaly

---
name: moomoo-technical-anomaly
description: >-
  Detects technical-analysis anomaly signals for a user-mentioned stock with
  `get_technical_unusual`, including K线形态 and indicator events such as CCI,
  KDJ, RSI, BIAS, ARBR, VR, PSY, OSC, WMSR, MACD, BOLL, and MA. Use when the
  user asks about 技术面情况、最近有什么技术信号、K线形态、形态识别、形态突破、金叉/死叉、
  超买超卖、MACD、RSI、KDJ、CCI、MA、BOLL、WMSR、VR、PSY、OSC、BIAS、ARBR，
  or gives a broad stock-anomaly request such as “英伟达异动”、“NVDA 异动”、
  “腾讯有没有异动/异常” without narrowing the dimension. For broad anomaly
  requests, this skill should be used together with `capital-anomaly` and
  `derivatives-anomaly`. Before calling the script, you must first normalize the
  user-mentioned stock name, Chinese company name, English company name, or
  ticker into a standard symbol such as `US.NVDA` or `HK.00700`.
metadata:
  version: 0.0.1
  author: Futu
license: MIT
---

# Technical Anomaly Skill

Detects technical-analysis anomalies for a specific stock and formats the result as a structured technical anomaly summary.

This skill is for **异动检测** rather than a regular technical overview. Focus on concrete abnormal events within the requested window. Do not add extra行情综述、基本面解释或投资建议.

If the user only says a broad request such as `英伟达异动`、`NVDA 异动`、`腾讯有没有异常` and does not specify a dimension, treat it as a bundled anomaly request. In that case, this skill should be used as one of the three default anomaly skills together with `capital-anomaly` and `derivatives-anomaly`.

---

## Workflow

### 1. Parse User Input

Extract the following from the user's request:

- `stock_target`: stock code, Chinese stock name, English company name, or ticker explicitly mentioned by the user
- `time_range`: default `7`; if the user says "最近 3 天" / "过去两周" / "last 5 days", convert it to a natural-day integer
- `indicator_filters`: optional; only extract when the user clearly asks for one or more specific indicators
- `language_id`: infer from the user's language

If the target stock is missing, ask a follow-up question instead of guessing.

### 2. Normalize the Stock Target into a Standard Symbol

Before calling the script, convert the user-mentioned stock target into a standard symbol such as `US.NVDA`, `HK.00700`, `SH.600519`, or `SZ.000001`.

Normalization rules:

- If the user already gives a fully qualified symbol like `US.NVDA` or `HK.00700`, use it directly.
- If the user gives a Chinese company name, English company name, or common ticker, map it to the matching market-prefixed symbol.
- If the symbol is ambiguous, ask a follow-up question instead of guessing.

Common mappings:

| User mention | Standard symbol |
|--------------|-----------------|
| 腾讯 | `HK.00700` |
| 阿里巴巴、阿里 | `HK.09988` |
| 苹果、Apple | `US.AAPL` |
| 特斯拉、Tesla | `US.TSLA` |
| 英伟达、NVIDIA | `US.NVDA` |
| 微软、Microsoft | `US.MSFT` |
| 谷歌、Google、Alphabet | `US.GOOG` |
| 亚马逊、Amazon | `US.AMZN` |
| Meta、脸书、Facebook | `US.META` |
| 台积电、TSM | `US.TSM` |
| 贵州茅台、茅台 | `SH.600519` |
| 宁德时代 | `SZ.300750` |

Ticker inference guidance:

- `NVDA`, `AAPL`, `TSLA`, `MSFT`, `GOOG`, `META` usually mean US stocks, so normalize to `US.NVDA`, `US.AAPL`, `US.TSLA`, `US.MSFT`, `US.GOOG`, `US.META`.
- `00700` by itself is ambiguous in plain text; when the context clearly refers to Tencent, normalize to `HK.00700`.
- If the same company has both HK and US listings and the user does not specify the market, ask a clarifying question.

### 3. Map Technical Intent to `indicator_filters`

Prefer these canonical `indicator_filters` values when the user clearly asks about a subset:

- `CCI`
- `KDJ`
- `BIAS`
- `AR`
- `BR`
- `VR`
- `PSY`
- `OSC`
- `WMSR`
- `MACD`
- `BOLL`
- `MA`
- `RSI6`
- `RSI12`
- `RSI24`

Selection guidance:

- If the user asks a broad technical question and does not limit indicators, omit `indicator_filters`.
- If the user asks about `MACD`, `金叉`, or `死叉`, include `MACD`.
- If the user asks about `RSI` or `超买超卖`, include `RSI6`, `RSI12`, and `RSI24`.
- If the user asks about `ARBR`, include both `AR` and `BR`.
- If the user asks about `BIAS24` or `乖离率`, include `BIAS`.
- If the user asks about one specific indicator, only pass that indicator's backend filter value when possible.

### 4. Infer `language_id`

Use the following language mapping:

- `0`: 简中
- `1`: 繁中
- `2`: 英文
- `4`: 泰语
- `5`: 日语

Default strategy:

- Chinese user -> `0`
- Traditional Chinese request -> `1`
- English user -> `2`
- If unclear, default to `0`

### 5. Call the Script

After extracting and normalizing the parameters, call the script with a Python 3 interpreter. Prefer `python3`; only fall back to `python` when `python3` is unavailable. This avoids the common macOS case where `python` is not installed or not on `PATH`.

Script entry:

```bash
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_technical_anomaly.py <STANDARD_SYMBOL> --time-range <DAYS> [--indicator-filters ...] [--language-id <ID>] --json
```

Examples:

```bash
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_technical_anomaly.py US.NVDA --time-range 7 --json
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_technical_anomaly.py HK.00700 --time-range 7 --indicator-filters MACD RSI6 RSI12 RSI24 --json
PYTHON_BIN="$(command -v python3 || command -v python)" && "$PYTHON_BIN" scripts/handle_technical_anomaly.py SH.600519 --time-range 14 --indicator-filters BOLL MA --json
```

### 6. Check the Result

- If the script exits successfully, use the returned data to build a structured technical-anomaly summary.
- If the script returns an error, surface the error message and do not fabricate results.
- If a requested indicator has no anomaly in the window, explicitly say `无异常`.

---

## Parameters

### Required

- `stock_symbol`: standard market-prefixed symbol, such as `US.NVDA`, `HK.00700`, `SH.600519`, `SZ.000001`

### Optional

- `time_range`: natural day window, default `7`
- `indicator_filters`: list of specific technical dimensions to inspect; omit for full scan
- `language_id`: output language, default `0`

---

## Output Rules

Present output by signal class. The response should cover:

- `K线形态`
- requested indicator classes, or the full set returned by the interface

Formatting rules:

- Always display `时间范围` as an absolute date range in the format `YYYY.M.D - YYYY.M.D`. Calculate the start date from the current date minus `time_range` days (e.g., if today is 2026.4.24 and time_range is 7, write `时间范围：2026.4.18 - 2026.4.24`).
- Show each class separately.
- If one class has multiple abnormal dates in the window, list them all in the same class.
- If one class has no anomaly in the window, write `无异常`.
- Preserve dates, pattern names, signal direction, probabilities, support/resistance, and interpretation from the tool output.
- Do not merge multiple indicator classes into one sentence.
- Do not invent thresholds or explanations beyond the returned content.
- If the user only asked about a subset of indicators, keep only `K线形态` plus the requested indicator classes.

---

## Preferred Response Template

```markdown
时间范围：{YYYY.M.D - YYYY.M.D}

- K线形态：{异常内容或“无异常”}
- MACD：{异常内容或“无异常”}
- RSI：{异常内容或“无异常”}
- CCI：{异常内容或“无异常”}
- KDJ：{异常内容或“无异常”}
- BIAS：{异常内容或“无异常”}
- ARBR：{异常内容或“无异常”}
- VR：{异常内容或“无异常”}
- PSY：{异常内容或“无异常”}
- OSC：{异常内容或“无异常”}
- WMSR：{异常内容或“无异常”}
- BOLL：{异常内容或“无异常”}
- MA：{异常内容或“无异常”}
```

When the user only asks for a subset, keep only `K线形态` plus the requested classes.

---

## Behavior Rules

1. Always normalize the user-mentioned stock target into a standard symbol before calling the script.
2. If the target stock is missing, ask a follow-up question.
3. If the market is ambiguous, ask a follow-up question instead of guessing.
4. If the user asks a broad technical question, omit `indicator_filters` and use the full interface.
5. Do not output raw JSON by default when talking to the user, even if the script returns JSON.
6. Do not interpret the result as investment advice or trading guidance.
7. Do not invent extra signal explanations beyond what the interface returns.

---

## Example User Requests

### Broad technical anomaly check

- "英伟达最近 7 天有什么技术面异动？"
- "看看腾讯最近的技术信号"
- "帮我查一下 Apple 最近有没有技术面异常"

Mapped request:

```json
{
  "stock_symbol": "US.NVDA",
  "time_range": 7,
  "language_id": 0
}
```

### MACD and RSI only

- "00700 最近 7 天 MACD 和 RSI 有没有异常？"
- "看看 NVDA 的 MACD、RSI 信号"

Mapped request:

```json
{
  "stock_symbol": "HK.00700",
  "time_range": 7,
  "indicator_filters": ["MACD", "RSI6", "RSI12", "RSI24"],
  "language_id": 0
}
```

### ARBR only

- "腾讯最近 ARBR 有异动吗？"

Mapped request:

```json
{
  "stock_symbol": "HK.00700",
  "time_range": 7,
  "indicator_filters": ["AR", "BR"],
  "language_id": 0
}
```

---

## Example Interpretation Style

```markdown
时间范围：2026.4.2-2026.4.9

- K线形态：在4.5，K线出现了“看涨持续三角形”形态，由高点逐渐降低和低点逐渐升高形成，表明市场力量在收敛后，多头占优，突破后可能继续上涨，上涨概率是84.5%，支撑位是2.41，压力位是2.52。
- MACD：无异常
- RSI：在4.2，RSI出现了金叉，预示着市场可能会迎来一波上涨；在4.8，RSI出现了死叉，暗示市场可能会进入下行趋势。
- CCI：在4.3，CCI突破+100进入超买区域，提示短期存在回调风险。
- KDJ：在4.6，KDJ三线在20以下形成金叉，发出超卖区反弹信号。
```
