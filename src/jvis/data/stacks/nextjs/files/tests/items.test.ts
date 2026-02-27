import { describe, it, expect } from 'vitest';

describe('Items API', () => {
  const BASE_URL = 'http://localhost:3000/api/items';

  describe('GET /api/items', () => {
    it('should return an array', async () => {
      const res = await fetch(BASE_URL);
      expect(res.status).toBe(200);
      const data = await res.json();
      expect(Array.isArray(data)).toBe(true);
    });
  });

  describe('POST /api/items', () => {
    it('should create an item', async () => {
      const res = await fetch(BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Test Item', description: 'A test' }),
      });
      expect(res.status).toBe(201);
      const data = await res.json();
      expect(data.name).toBe('Test Item');
      expect(data).toHaveProperty('id');
    });

    it('should return 400 without name', async () => {
      const res = await fetch(BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: 'no name' }),
      });
      expect(res.status).toBe(400);
    });
  });

  describe('CRUD operations', () => {
    it('should get, update, and delete an item', async () => {
      // Create
      const createRes = await fetch(BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'CRUD Test' }),
      });
      const created = await createRes.json();

      // Get
      const getRes = await fetch(`${BASE_URL}/${created.id}`);
      expect(getRes.status).toBe(200);
      expect((await getRes.json()).name).toBe('CRUD Test');

      // Update
      const updateRes = await fetch(`${BASE_URL}/${created.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Updated' }),
      });
      expect(updateRes.status).toBe(200);
      expect((await updateRes.json()).name).toBe('Updated');

      // Delete
      const deleteRes = await fetch(`${BASE_URL}/${created.id}`, { method: 'DELETE' });
      expect(deleteRes.status).toBe(204);
    });
  });
});
