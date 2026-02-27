import type { Item } from '../../domain/entities/item.js';
import type { CreateItemDto, UpdateItemDto } from '../../application/dto/item.dto.js';
import type { IItemRepository } from '../../domain/interfaces/item-repository.interface.js';
import { prisma } from '../database/prisma-client.js';

export class ItemRepository implements IItemRepository {
  async create(data: CreateItemDto): Promise<Item> {
    return prisma.item.create({
      data: {
        name: data.name,
        description: data.description ?? null,
      },
    });
  }

  async findById(id: string): Promise<Item | null> {
    return prisma.item.findUnique({ where: { id } });
  }

  async findAll(): Promise<Item[]> {
    return prisma.item.findMany({ orderBy: { createdAt: 'desc' } });
  }

  async update(id: string, data: UpdateItemDto): Promise<Item> {
    return prisma.item.update({ where: { id }, data });
  }

  async delete(id: string): Promise<void> {
    await prisma.item.delete({ where: { id } });
  }
}
