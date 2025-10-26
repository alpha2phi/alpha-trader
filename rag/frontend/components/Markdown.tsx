'use client';
import { useEffect, useState } from 'react';
import { remark } from 'remark';
// @ts-ignore
import html from 'remark-html';

export default function Markdown({ md }: { md: string }) {
  const [content, setContent] = useState('');
  useEffect(() => {
    (async () => {
      const processed = await remark().use(html).process(md);
      setContent(String(processed));
    })();
  }, [md]);
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
}
