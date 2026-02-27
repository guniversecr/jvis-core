import axios from 'axios';
import type { Item, CreateItemInput, UpdateItemInput } from '../types/item';
import { config } from '../utils/config';

const client = axios.create({
  baseURL: config.apiBaseUrl,
  headers: { 'Content-Type': 'application/json' },
});

export const itemsApi = {
  async list(): Promise<Item[]> {
    const { data } = await client.get<Item[]>('/items');
    return data;
  },

  async getById(id: string): Promise<Item> {
    const { data } = await client.get<Item>(`/items/${id}`);
    return data;
  },

  async create(input: CreateItemInput): Promise<Item> {
    const { data } = await client.post<Item>('/items', input);
    return data;
  },

  async update(id: string, input: UpdateItemInput): Promise<Item> {
    const { data } = await client.patch<Item>(`/items/${id}`, input);
    return data;
  },

  async delete(id: string): Promise<void> {
    await client.delete(`/items/${id}`);
  },
};
