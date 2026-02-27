import { useState, useEffect } from 'preact/hooks';
import type { Item, CreateItemInput } from '../types/item';
import { itemsApi } from '../services/api';
import ItemForm from './ItemForm';
import ItemList from './ItemList';

export default function ItemApp() {
  const [items, setItems] = useState<Item[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadItems = async () => {
    try {
      setLoading(true);
      const data = await itemsApi.list();
      setItems(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load items');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadItems();
  }, []);

  const handleCreate = async (input: CreateItemInput) => {
    try {
      await itemsApi.create(input);
      await loadItems();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create item');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await itemsApi.delete(id);
      await loadItems();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete item');
    }
  };

  return (
    <div>
      <h1>Items</h1>
      {error && <p class="error-message">{error}</p>}
      <ItemForm onSubmit={handleCreate} />
      {loading ? <p>Loading...</p> : <ItemList items={items} onDelete={handleDelete} />}
    </div>
  );
}
