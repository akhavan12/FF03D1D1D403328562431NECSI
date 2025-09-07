'use client';
import Link from 'next/link';

type MenuItem = { label: string; href: string };
type Menu = { brand?: string; items: MenuItem[] };

export default function Navbar({ menu }: { menu: Menu }) {
  return (
    <nav style={{
      display: 'flex',
      alignItems: 'center',
      gap: '1rem',
      padding: '0.75rem 1rem',
      borderBottom: '1px solid #eee',
      position: 'sticky',
      top: 0,
      backdropFilter: 'blur(6px)',
      background: 'rgba(255,255,255,0.8)',
      zIndex: 1000
    }}>
      <strong style={{ marginRight: 'auto' }}>
        <Link href="/">{menu.brand ?? 'Site'}</Link>
      </strong>
      {menu.items?.map((it) => (
        <Link key={it.href} href={it.href}>
          {it.label}
        </Link>
      ))}
    </nav>
  );
}
