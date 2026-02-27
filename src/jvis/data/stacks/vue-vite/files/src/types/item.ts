export interface Item {
  id: string;
  name: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface CreateItemInput {
  name: string;
  description?: string | null;
}

export interface UpdateItemInput {
  name?: string;
  description?: string | null;
}
