import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ItemService } from '../../src/application/use-cases/item.service.js';
import { NotFoundError } from '../../src/domain/errors/app-error.js';

const mockRepository = {
  create: vi.fn(),
  findById: vi.fn(),
  findAll: vi.fn(),
  update: vi.fn(),
  delete: vi.fn(),
};

describe('ItemService', () => {
  let service: ItemService;

  beforeEach(() => {
    vi.clearAllMocks();
    service = new ItemService(mockRepository as never);
  });

  describe('create', () => {
    it('should create an item', async () => {
      const data = { name: 'Test Item', description: 'A test item' };
      const expected = { id: '1', ...data, createdAt: new Date(), updatedAt: new Date() };
      mockRepository.create.mockResolvedValue(expected);

      const result = await service.create(data);

      expect(result).toEqual(expected);
      expect(mockRepository.create).toHaveBeenCalledWith(data);
    });
  });

  describe('getById', () => {
    it('should return an item by id', async () => {
      const expected = { id: '1', name: 'Test', description: null, createdAt: new Date(), updatedAt: new Date() };
      mockRepository.findById.mockResolvedValue(expected);

      const result = await service.getById('1');

      expect(result).toEqual(expected);
    });

    it('should throw NotFoundError when item does not exist', async () => {
      mockRepository.findById.mockResolvedValue(null);

      await expect(service.getById('999')).rejects.toThrow(NotFoundError);
    });
  });

  describe('list', () => {
    it('should return all items', async () => {
      const items = [
        { id: '1', name: 'Item 1', description: null, createdAt: new Date(), updatedAt: new Date() },
        { id: '2', name: 'Item 2', description: 'desc', createdAt: new Date(), updatedAt: new Date() },
      ];
      mockRepository.findAll.mockResolvedValue(items);

      const result = await service.list();

      expect(result).toHaveLength(2);
    });
  });

  describe('delete', () => {
    it('should delete an existing item', async () => {
      mockRepository.findById.mockResolvedValue({ id: '1', name: 'Test' });
      mockRepository.delete.mockResolvedValue(undefined);

      await service.delete('1');

      expect(mockRepository.delete).toHaveBeenCalledWith('1');
    });

    it('should throw NotFoundError when deleting non-existent item', async () => {
      mockRepository.findById.mockResolvedValue(null);

      await expect(service.delete('999')).rejects.toThrow(NotFoundError);
    });
  });
});
