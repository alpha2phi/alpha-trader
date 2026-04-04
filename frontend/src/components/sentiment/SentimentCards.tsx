import React from "react";
import { useSentiment } from "../../services/hooks/useSentiment";
import { LoadingSpinner, ErrorState, StaleBadge } from "../shared/status";

function Card({
  title,
  value,
  subtitle,
  isStale,
  onRetry,
}: {
  title: string;
  value: React.ReactNode;
  subtitle?: string;
  isStale?: boolean;
  onRetry: () => void;
}) {
  return (
    <div>
      <div>{title}</div>
      <div>{value}</div>
      {subtitle && <div>{subtitle}</div>}
      {isStale && <StaleBadge />}
      <button onClick={onRetry}>Retry</button>
    </div>
  );
}

export function SentimentCards() {
  const { data, isLoading, error, refetch } = useSentiment();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorState message={(error as Error).message} />;
  if (!data) return <ErrorState message="No data" />;

  const fg = data.fear_greed;
  const vix = data.vix;

  return (
    <div>
      <Card
        title="Fear & Greed"
        value={`${fg.score} (${fg.category})`}
        subtitle={`Updated: ${fg.updated_at}`}
        isStale={fg.cache_state === "stale"}
        onRetry={() => refetch()}
      />
      <Card
        title="VIX"
        value={`${vix.level.toFixed(2)}`}
        subtitle={`Δ ${vix.abs_change.toFixed(2)} (${vix.pct_change.toFixed(2)}%) • Updated: ${vix.updated_at}`}
        isStale={vix.cache_state === "stale"}
        onRetry={() => refetch()}
      />
    </div>
  );
}
