import React from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { SentimentCards } from "../components/sentiment/SentimentCards";
import { getQueryClient } from "../services/api-client";

const queryClient = getQueryClient();

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <main>
        <h1>Market Sentiment Dashboard</h1>
        <SentimentCards />
      </main>
    </QueryClientProvider>
  );
}
