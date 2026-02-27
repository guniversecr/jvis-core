import { Router } from 'express';
import { ItemController } from '../controllers/item.controller.js';
import { ItemService } from '../../application/use-cases/item.service.js';
import { validateId } from '../middleware/validate-id.js';

const controller = new ItemController(new ItemService());

export const itemsRouter = Router();

itemsRouter.post('/', controller.create);
itemsRouter.get('/', controller.list);
itemsRouter.get('/:id', validateId, controller.getById);
itemsRouter.patch('/:id', validateId, controller.update);
itemsRouter.delete('/:id', validateId, controller.delete);
