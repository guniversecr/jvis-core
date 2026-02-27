import type { Item } from '../../types/item';
import { ItemCard } from './ItemCard';

interface ItemListProps {
  items: Item[];
  onDelete: (id: string) => void;
}

export function ItemList({ items, onDelete }: ItemListProps) {
  if (items.length === 0) {
    return <p>No items yet. Create one above.</p>;
  }

  return (
    <ul className="item-list">
      {items.map((item) => (
        <li key={item.id}>
          <ItemCard item={item} onDelete={onDelete} />
        </li>
      ))}
    </ul>
  );
}
