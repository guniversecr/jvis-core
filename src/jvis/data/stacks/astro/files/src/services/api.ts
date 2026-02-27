import { config } from '../utils/config';
import type { Item, CreateItemInput, UpdateItemInput } from '../types/item';

const BASE_URL = `${config.apiBaseUrl}/items`;

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(error.message || `Request failed: ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const itemsApi = {
  list: () => request<Item[]>(BASE_URL),
  get: (id: string) => request<Item>(`${BASE_URL}/${id}`),
  create: (input: CreateItemInput) =>
    request<Item>(BASE_URL, { method: 'POST', body: JSON.stringify(input) }),
  update: (id: string, input: UpdateItemInput) =>
    request<Item>(`${BASE_URL}/${id}`, { method: 'PATCH', body: JSON.stringify(input) }),
  delete: (id: string) =>
    request<void>(`${BASE_URL}/${id}`, { method: 'DELETE' }),
};
