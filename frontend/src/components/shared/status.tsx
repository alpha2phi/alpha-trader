import React from "react";

export function LoadingSpinner() {
  return <div aria-busy="true">Loading...</div>;
}

export function ErrorState({ message }: { message: string }) {
  return <div role="alert">Error: {message}</div>;
}

export function StaleBadge() {
  return <span title="Data may be stale">Stale</span>;
}
