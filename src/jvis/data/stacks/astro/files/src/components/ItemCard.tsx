import type { Item } from '../types/item';

interface Props {
  item: Item;
  onDelete: (id: string) => void;
}

export default function ItemCard({ item, onDelete }: Props) {
  return (
    <div class="item-card">
      <div>
        <strong>{item.name}</strong>
        {item.description && <p>{item.description}</p>}
      </div>
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </div>
  );
}
