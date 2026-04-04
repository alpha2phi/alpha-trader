import { useQuery } from "@tanstack/react-query";
import { fetchJson } from "../api-client";

export type CacheState = "fresh" | "stale";

type FearGreed = {
  score: number;
  category: string;
  updated_at: string;
  cache_state: CacheState;
};

type Vix = {
  level: number;
  abs_change: number;
  pct_change: number;
  updated_at: string;
  cache_state: CacheState;
};

export type SentimentSnapshot = {
  fear_greed: FearGreed;
  vix: Vix;
};

export function useSentiment() {
  return useQuery<SentimentSnapshot>({
    queryKey: ["sentiment"],
    queryFn: () => fetchJson<SentimentSnapshot>("/sentiment"),
    staleTime: 1000 * 60 * 5, // tolerate short staleness client-side
  });
}
