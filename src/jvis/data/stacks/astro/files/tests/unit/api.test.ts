import { describe, it, expect, vi, beforeEach } from 'vitest';

const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

vi.mock('../../src/utils/config', () => ({
  config: {
    apiBaseUrl: 'http://localhost:3001/api',
    appName: 'test-app',
  },
}));

import { itemsApi } from '../../src/services/api';

describe('itemsApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should list items', async () => {
    const mockItems = [
      { id: '1', name: 'Item 1', description: null, createdAt: '', updatedAt: '' },
    ];
    mockFetch.mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockItems),
    });

    const result = await itemsApi.list();

    expect(result).toEqual(mockItems);
    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:3001/api/items',
      expect.objectContaining({ headers: { 'Content-Type': 'application/json' } }),
    );
  });

  it('should create an item', async () => {
    const mockItem = { id: '1', name: 'New', description: null, createdAt: '', updatedAt: '' };
    mockFetch.mockResolvedValue({
      ok: true,
      status: 201,
      json: () => Promise.resolve(mockItem),
    });

    const result = await itemsApi.create({ name: 'New' });

    expect(result).toEqual(mockItem);
    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:3001/api/items',
      expect.objectContaining({ method: 'POST' }),
    );
  });

  it('should throw on error response', async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: () => Promise.resolve({ message: 'Server error' }),
    });

    await expect(itemsApi.list()).rejects.toThrow('Server error');
  });
});
