import type { Item } from '../entities/item.js';
import type { CreateItemDto, UpdateItemDto } from '../../application/dto/item.dto.js';

export interface IItemRepository {
  create(data: CreateItemDto): Promise<Item>;
  findById(id: string): Promise<Item | null>;
  findAll(): Promise<Item[]>;
  update(id: string, data: UpdateItemDto): Promise<Item>;
  delete(id: string): Promise<void>;
}
