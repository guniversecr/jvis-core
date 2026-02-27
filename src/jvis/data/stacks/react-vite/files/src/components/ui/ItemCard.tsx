import { useState } from 'react';
import type { Item } from '../../types/item';

interface ItemCardProps {
  item: Item;
  onDelete: (id: string) => Promise<void>;
}

export function ItemCard({ item, onDelete }: ItemCardProps) {
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await onDelete(item.id);
    } catch {
      setDeleting(false);
    }
  };

  return (
    <div className="item-card">
      <h3>{item.name}</h3>
      {item.description && <p>{item.description}</p>}
      <button type="button" onClick={handleDelete} disabled={deleting}>
        {deleting ? 'Deleting...' : 'Delete'}
      </button>
    </div>
  );
}
