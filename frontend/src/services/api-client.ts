import { QueryClient } from "@tanstack/react-query";

const queryClient = new QueryClient();

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export function getQueryClient(): QueryClient {
  return queryClient;
}

export async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}
