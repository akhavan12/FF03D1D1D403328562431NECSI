import './globals.css';
import Navbar from '@/components/Navbar';
import fs from 'fs/promises';
import path from 'path';

export const metadata = {
  title: 'NECSI',
  description: 'JSON-driven Next.js site',
};

async function readMenu() {
  const file = await fs.readFile(path.join(process.cwd(), 'content', 'menu.json'), 'utf8');
  return JSON.parse(file);
}

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const menu = await readMenu();

  return (
    <html lang="en">
      <body>
        <Navbar menu={menu} />
        {children}
      </body>
    </html>
  );
}
