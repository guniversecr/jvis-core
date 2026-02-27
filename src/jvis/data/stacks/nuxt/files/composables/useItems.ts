import type { Item, CreateItemDto, UpdateItemDto } from '~/types/item';

export function useItems() {
  const items = ref<Item[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchItems() {
    loading.value = true;
    error.value = null;
    try {
      items.value = await $fetch<Item[]>('/api/items');
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch items';
    } finally {
      loading.value = false;
    }
  }

  async function createItem(dto: CreateItemDto) {
    await $fetch<Item>('/api/items', { method: 'POST', body: dto });
    await fetchItems();
  }

  async function updateItem(id: string, dto: UpdateItemDto) {
    await $fetch<Item>(`/api/items/${id}`, { method: 'PATCH', body: dto });
    await fetchItems();
  }

  async function deleteItem(id: string) {
    await $fetch(`/api/items/${id}`, { method: 'DELETE' });
    await fetchItems();
  }

  return { items, loading, error, fetchItems, createItem, updateItem, deleteItem };
}
