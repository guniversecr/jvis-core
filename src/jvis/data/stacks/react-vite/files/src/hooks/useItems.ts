import { useState, useEffect, useCallback } from 'react';
import type { Item, CreateItemInput } from '../types/item';
import { itemsApi } from '../services/api';

export function useItems() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await itemsApi.list();
      setItems(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch items');
    } finally {
      setLoading(false);
    }
  }, []);

  const createItem = useCallback(async (input: CreateItemInput) => {
    setError(null);
    try {
      const item = await itemsApi.create(input);
      setItems((prev) => [item, ...prev]);
      return item;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create item');
      throw err;
    }
  }, []);

  const deleteItem = useCallback(async (id: string) => {
    setError(null);
    try {
      await itemsApi.delete(id);
      setItems((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete item');
      throw err;
    }
  }, []);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  return { items, loading, error, fetchItems, createItem, deleteItem };
}
