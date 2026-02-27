import { describe, it, expect } from 'vitest';

describe('Items API', () => {
  const baseUrl = process.env.NUXT_TEST_URL || 'http://localhost:3000';

  let createdId: string;

  it('should create an item', async () => {
    const res = await fetch(`${baseUrl}/api/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Test Item', description: 'A test item' }),
    });

    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body).toHaveProperty('id');
    expect(body.name).toBe('Test Item');
    createdId = body.id;
  });

  it('should list all items', async () => {
    const res = await fetch(`${baseUrl}/api/items`);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(Array.isArray(body)).toBe(true);
  });

  it('should get an item by id', async () => {
    const res = await fetch(`${baseUrl}/api/items/${createdId}`);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.name).toBe('Test Item');
  });

  it('should update an item', async () => {
    const res = await fetch(`${baseUrl}/api/items/${createdId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Updated Item' }),
    });

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.name).toBe('Updated Item');
  });

  it('should delete an item', async () => {
    const res = await fetch(`${baseUrl}/api/items/${createdId}`, {
      method: 'DELETE',
    });

    expect(res.status).toBe(204);
  });

  it('should return 404 for non-existent item', async () => {
    const res = await fetch(`${baseUrl}/api/items/non-existent-id`);

    expect(res.status).toBe(404);
  });
});
