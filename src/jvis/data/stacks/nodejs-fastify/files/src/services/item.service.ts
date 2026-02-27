import type { Item } from '../domain/entities/item.js';
import { NotFoundError } from '../domain/errors/app-error.js';
import { prisma } from '../infrastructure/prisma-client.js';

export class ItemService {
  async create(data: { name: string; description?: string | null }): Promise<Item> {
    return prisma.item.create({ data });
  }

  async list(): Promise<Item[]> {
    return prisma.item.findMany({ orderBy: { createdAt: 'desc' } });
  }

  async getById(id: string): Promise<Item> {
    const item = await prisma.item.findUnique({ where: { id } });
    if (!item) {
      throw new NotFoundError('Item', id);
    }
    return item;
  }

  async update(id: string, data: { name?: string; description?: string | null }): Promise<Item> {
    await this.getById(id);
    return prisma.item.update({ where: { id }, data });
  }

  async delete(id: string): Promise<void> {
    await this.getById(id);
    await prisma.item.delete({ where: { id } });
  }
}
