import type { Item } from '../types/item';
import ItemCard from './ItemCard';

interface Props {
  items: Item[];
  onDelete: (id: string) => void;
}

export default function ItemList({ items, onDelete }: Props) {
  if (items.length === 0) {
    return <p>No items yet. Create one above.</p>;
  }

  return (
    <ul class="item-list">
      {items.map((item) => (
        <li key={item.id}>
          <ItemCard item={item} onDelete={onDelete} />
        </li>
      ))}
    </ul>
  );
}
