import Link from 'next/link';
import { prisma } from '@/lib/db';

export default async function ItemsPage() {
  const items = await prisma.item.findMany({ orderBy: { createdAt: 'desc' } });

  return (
    <main>
      <h1>Items</h1>
      <Link href="/">Back to Home</Link>

      {items.length === 0 ? (
        <p>No items yet. Create one via POST /api/items.</p>
      ) : (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <strong>{item.name}</strong>
              {item.description && <span> — {item.description}</span>}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
