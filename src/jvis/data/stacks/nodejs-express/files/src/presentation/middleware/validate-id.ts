import type { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { ValidationError } from '../../domain/errors/app-error.js';

const IdSchema = z.string().min(1, 'ID is required').regex(/^[a-z0-9]+$/i, 'Invalid ID format');

export function validateId(req: Request, _res: Response, next: NextFunction): void {
  const result = IdSchema.safeParse(req.params.id);
  if (!result.success) {
    next(new ValidationError(result.error.issues.map((i) => i.message).join(', ')));
    return;
  }
  next();
}
