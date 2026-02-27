import { writable } from 'svelte/store';
import type { Item, CreateItemInput } from '../types/item';
import { itemsApi } from '../services/api';

export const items = writable<Item[]>([]);
export const loading = writable(false);
export const error = writable<string | null>(null);

export async function fetchItems() {
  loading.set(true);
  error.set(null);
  try {
    const data = await itemsApi.list();
    items.set(data);
  } catch (e: unknown) {
    error.set(e instanceof Error ? e.message : 'Failed to fetch items');
  } finally {
    loading.set(false);
  }
}

export async function createItem(input: CreateItemInput) {
  await itemsApi.create(input);
  await fetchItems();
}

export async function deleteItem(id: string) {
  await itemsApi.delete(id);
  await fetchItems();
}
