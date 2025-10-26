'use client';

import { useState } from 'react';
import { runDaily } from '../lib/api';
import Markdown from '../components/Markdown';

export default function Page() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [shortMd, setShortMd] = useState<string | null>(null);
  const [longMd, setLongMd] = useState<string | null>(null);
  const [note, setNote] = useState<string | null>(null);

  async function onRun() {
    try {
      setLoading(true); setError(null);
      const res = await runDaily();
      setShortMd(res.short_premium_table_md);
      setLongMd(res.long_term_table_md);
      setNote(res.notes || null);
    } catch (e:any) {
      setError(e?.message || 'Failed to run');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button onClick={onRun} disabled={loading}
        style={{ padding: '10px 16px', borderRadius: 12, border: '1px solid #ddd', cursor: 'pointer' }}>
        {loading ? 'Running…' : 'Run Daily Screen'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {note && <p style={{ marginTop: 12, opacity: 0.8 }}>Note: {note}</p>}

      <section style={{ marginTop: 24 }}>
        <h2>Short-Premium Candidates</h2>
        {shortMd ? <Markdown md={shortMd} /> : <p>No results yet. Click “Run Daily Screen”.</p>}
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Long-Term Buys</h2>
        {longMd ? <Markdown md={longMd} /> : <p>No results yet.</p>}
      </section>
    </div>
  );
}
