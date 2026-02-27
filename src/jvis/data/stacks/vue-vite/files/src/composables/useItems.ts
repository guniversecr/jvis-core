import { ref, onMounted } from 'vue';
import type { Item, CreateItemInput } from '../types/item';
import { itemsApi } from '../services/api';

export function useItems() {
  const items = ref<Item[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchItems() {
    loading.value = true;
    error.value = null;
    try {
      items.value = await itemsApi.list();
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch items';
    } finally {
      loading.value = false;
    }
  }

  async function createItem(input: CreateItemInput) {
    await itemsApi.create(input);
    await fetchItems();
  }

  async function deleteItem(id: string) {
    await itemsApi.delete(id);
    await fetchItems();
  }

  onMounted(fetchItems);

  return { items, loading, error, createItem, deleteItem };
}
