export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'ui-sans-serif, system-ui', margin: 0 }}>
        <div style={{ maxWidth: 980, margin: '0 auto', padding: 24 }}>
          <h1 style={{ fontSize: 28, marginBottom: 8 }}>RAG Options Trader</h1>
          <p style={{ opacity: 0.8, marginBottom: 24 }}>tastytrade-style screening with RAG + tool numerics</p>
          {children}
        </div>
      </body>
    </html>
  );
}
