import { describe, it, expect, vi, beforeEach } from 'vitest';
import { get } from 'svelte/store';

vi.mock('../../src/lib/services/api', () => ({
  itemsApi: {
    list: vi.fn(),
    create: vi.fn(),
    delete: vi.fn(),
  },
}));

import { items, loading, error, fetchItems } from '../../src/lib/stores/items';
import { itemsApi } from '../../src/lib/services/api';

const mockApi = vi.mocked(itemsApi);

describe('items store', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    items.set([]);
    loading.set(false);
    error.set(null);
  });

  it('should fetch items', async () => {
    const mockItems = [
      { id: '1', name: 'Item 1', description: null, createdAt: '', updatedAt: '' },
    ];
    mockApi.list.mockResolvedValue(mockItems);

    await fetchItems();

    expect(get(items)).toEqual(mockItems);
    expect(get(loading)).toBe(false);
    expect(get(error)).toBeNull();
  });

  it('should handle fetch error', async () => {
    mockApi.list.mockRejectedValue(new Error('Network error'));

    await fetchItems();

    expect(get(items)).toEqual([]);
    expect(get(error)).toBe('Network error');
  });
});
