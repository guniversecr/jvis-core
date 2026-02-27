import type { FastifyInstance } from 'fastify';
import { ItemService } from '../services/item.service.js';
import { AppError } from '../domain/errors/app-error.js';
import {
  createItemSchema,
  listItemsSchema,
  getItemSchema,
  updateItemSchema,
  deleteItemSchema,
} from '../schemas/item.schema.js';

const service = new ItemService();

export async function itemRoutes(app: FastifyInstance): Promise<void> {
  app.post('/items', { schema: createItemSchema }, async (request, reply) => {
    const item = await service.create(request.body as { name: string; description?: string | null });
    return reply.status(201).send(item);
  });

  app.get('/items', { schema: listItemsSchema }, async () => {
    return service.list();
  });

  app.get<{ Params: { id: string } }>('/items/:id', { schema: getItemSchema }, async (request) => {
    return service.getById(request.params.id);
  });

  app.patch<{ Params: { id: string } }>('/items/:id', { schema: updateItemSchema }, async (request) => {
    return service.update(request.params.id, request.body as { name?: string; description?: string | null });
  });

  app.delete<{ Params: { id: string } }>('/items/:id', { schema: deleteItemSchema }, async (request, reply) => {
    await service.delete(request.params.id);
    return reply.status(204).send();
  });

  app.setErrorHandler((error, _request, reply) => {
    if (error instanceof AppError) {
      return reply.status(error.statusCode).send({
        error: error.code,
        message: error.message,
      });
    }
    app.log.error(error);
    return reply.status(500).send({ error: 'INTERNAL_ERROR', message: 'Internal server error' });
  });
}
