import { useItems } from '../hooks/useItems';
import { ItemList } from '../components/ui/ItemList';
import { ItemForm } from '../components/ui/ItemForm';

export function HomePage() {
  const { items, loading, error, createItem, deleteItem } = useItems();

  return (
    <div>
      <h2>Items</h2>
      <ItemForm onSubmit={createItem} />
      {error && <p className="error-message">{error}</p>}
      {loading ? <p>Loading...</p> : <ItemList items={items} onDelete={deleteItem} />}
    </div>
  );
}
