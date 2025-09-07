type Block =
  | { type: 'heading'; level?: 1|2|3|4|5|6; text: string }
  | { type: 'paragraph'; text: string }
  | { type: 'image'; src: string; alt?: string }
  | { type: 'list'; ordered?: boolean; items: string[] }
  | { type: 'html'; html: string };

export default function PageContent({ blocks }: { blocks: Block[] }) {
  return (
    <div style={{ padding: '1rem', maxWidth: 'var(--maxw)', margin: '0 auto' }}>
      {blocks?.map((b, i) => {
        if (b.type === 'heading') {
          const Tag = (`h${b.level ?? 2}` as keyof JSX.IntrinsicElements);
          return <Tag key={i}>{b.text}</Tag>;
        }
        if (b.type === 'paragraph') {
          return <p key={i} style={{ lineHeight: 1.7 }}>{b.text}</p>;
        }
        if (b.type === 'image') {
          return (
            <figure key={i} style={{ margin: '1rem 0' }}>
              <img src={b.src} alt={b.alt ?? ''} style={{ maxWidth: '100%', height: 'auto', display: 'block' }} />
              {b.alt && <figcaption style={{ fontSize: 12, color: '#666' }}>{b.alt}</figcaption>}
            </figure>
          );
        }
        if (b.type === 'list') {
          return b.ordered ? (
            <ol key={i}>{b.items.map((x, j) => <li key={j}>{x}</li>)}</ol>
          ) : (
            <ul key={i}>{b.items.map((x, j) => <li key={j}>{x}</li>)}</ul>
          );
        }
        if (b.type === 'html') {
          return <div key={i} dangerouslySetInnerHTML={{ __html: b.html }} />;
        }
        return null;
      })}
    </div>
  );
}
