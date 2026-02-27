export interface Item {
  id: string;
  name: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface CreateItemDto {
  name: string;
  description?: string;
}

export interface UpdateItemDto {
  name?: string;
  description?: string;
}
