import type { CreateItemDto, UpdateItemDto } from '../dto/item.dto.js';
import type { Item } from '../../domain/entities/item.js';
import type { IItemRepository } from '../../domain/interfaces/item-repository.interface.js';
import { NotFoundError } from '../../domain/errors/app-error.js';
import { ItemRepository } from '../../infrastructure/repositories/item.repository.js';

export class ItemService {
  private readonly repository: IItemRepository;

  constructor(repository?: IItemRepository) {
    this.repository = repository ?? new ItemRepository();
  }

  async create(data: CreateItemDto): Promise<Item> {
    return this.repository.create(data);
  }

  async getById(id: string): Promise<Item> {
    const item = await this.repository.findById(id);
    if (!item) {
      throw new NotFoundError('Item', id);
    }
    return item;
  }

  async list(): Promise<Item[]> {
    return this.repository.findAll();
  }

  async update(id: string, data: UpdateItemDto): Promise<Item> {
    await this.getById(id);
    return this.repository.update(id, data);
  }

  async delete(id: string): Promise<void> {
    await this.getById(id);
    return this.repository.delete(id);
  }
}
