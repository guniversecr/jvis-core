import { config } from '../config';
import type { Item, CreateItemInput, UpdateItemInput } from '../types/item';

const baseUrl = config.apiBaseUrl;

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${baseUrl}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const itemsApi = {
  list: () => request<Item[]>('/items'),
  getById: (id: string) => request<Item>(`/items/${id}`),
  create: (input: CreateItemInput) => request<Item>('/items', { method: 'POST', body: JSON.stringify(input) }),
  update: (id: string, input: UpdateItemInput) => request<Item>(`/items/${id}`, { method: 'PATCH', body: JSON.stringify(input) }),
  delete: (id: string) => request<void>(`/items/${id}`, { method: 'DELETE' }),
};
