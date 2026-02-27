import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateItemDto } from './dto/create-item.dto';
import { UpdateItemDto } from './dto/update-item.dto';
import type { Item } from './entities/item.entity';

@Injectable()
export class ItemsService {
  constructor(private readonly prisma: PrismaService) {}

  async create(dto: CreateItemDto): Promise<Item> {
    return this.prisma.item.create({ data: dto });
  }

  async findAll(): Promise<Item[]> {
    return this.prisma.item.findMany({ orderBy: { createdAt: 'desc' } });
  }

  async findOne(id: string): Promise<Item> {
    const item = await this.prisma.item.findUnique({ where: { id } });
    if (!item) {
      throw new NotFoundException(`Item with id '${id}' not found`);
    }
    return item;
  }

  async update(id: string, dto: UpdateItemDto): Promise<Item> {
    await this.findOne(id);
    return this.prisma.item.update({ where: { id }, data: dto });
  }

  async remove(id: string): Promise<void> {
    await this.findOne(id);
    await this.prisma.item.delete({ where: { id } });
  }
}
