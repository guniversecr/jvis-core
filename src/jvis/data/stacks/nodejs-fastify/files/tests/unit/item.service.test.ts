import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ItemService } from '../../src/services/item.service.js';

vi.mock('../../src/infrastructure/prisma-client.js', () => ({
  prisma: {
    item: {
      create: vi.fn(),
      findMany: vi.fn(),
      findUnique: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    },
  },
}));

import { prisma } from '../../src/infrastructure/prisma-client.js';

const mockPrisma = vi.mocked(prisma);

describe('ItemService', () => {
  let service: ItemService;

  beforeEach(() => {
    vi.clearAllMocks();
    service = new ItemService();
  });

  describe('create', () => {
    it('should create an item', async () => {
      const data = { name: 'Test Item', description: 'A test item' };
      const expected = { id: '1', ...data, createdAt: new Date(), updatedAt: new Date() };
      mockPrisma.item.create.mockResolvedValue(expected);

      const result = await service.create(data);

      expect(result).toEqual(expected);
      expect(mockPrisma.item.create).toHaveBeenCalledWith({ data });
    });
  });

  describe('list', () => {
    it('should return all items', async () => {
      const items = [
        { id: '1', name: 'Item 1', description: null, createdAt: new Date(), updatedAt: new Date() },
        { id: '2', name: 'Item 2', description: 'desc', createdAt: new Date(), updatedAt: new Date() },
      ];
      mockPrisma.item.findMany.mockResolvedValue(items);

      const result = await service.list();

      expect(result).toHaveLength(2);
    });
  });

  describe('getById', () => {
    it('should return an item by id', async () => {
      const expected = { id: '1', name: 'Test', description: null, createdAt: new Date(), updatedAt: new Date() };
      mockPrisma.item.findUnique.mockResolvedValue(expected);

      const result = await service.getById('1');

      expect(result).toEqual(expected);
    });

    it('should throw when item not found', async () => {
      mockPrisma.item.findUnique.mockResolvedValue(null);

      await expect(service.getById('999')).rejects.toThrow('not found');
    });
  });

  describe('delete', () => {
    it('should delete an existing item', async () => {
      mockPrisma.item.findUnique.mockResolvedValue({ id: '1', name: 'Test', description: null, createdAt: new Date(), updatedAt: new Date() });
      mockPrisma.item.delete.mockResolvedValue({ id: '1', name: 'Test', description: null, createdAt: new Date(), updatedAt: new Date() });

      await service.delete('1');

      expect(mockPrisma.item.delete).toHaveBeenCalledWith({ where: { id: '1' } });
    });
  });
});
