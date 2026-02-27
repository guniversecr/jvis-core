import type { FastifySchema } from 'fastify';

const itemProperties = {
  id: { type: 'string' },
  name: { type: 'string' },
  description: { type: ['string', 'null'] },
  createdAt: { type: 'string', format: 'date-time' },
  updatedAt: { type: 'string', format: 'date-time' },
} as const;

const itemResponse = {
  type: 'object',
  properties: itemProperties,
};

export const createItemSchema: FastifySchema = {
  body: {
    type: 'object',
    required: ['name'],
    properties: {
      name: { type: 'string', minLength: 1 },
      description: { type: ['string', 'null'] },
    },
  },
  response: { 201: itemResponse },
};

export const listItemsSchema: FastifySchema = {
  response: {
    200: {
      type: 'array',
      items: itemResponse,
    },
  },
};

export const getItemSchema: FastifySchema = {
  params: {
    type: 'object',
    required: ['id'],
    properties: { id: { type: 'string' } },
  },
  response: { 200: itemResponse },
};

export const updateItemSchema: FastifySchema = {
  params: {
    type: 'object',
    required: ['id'],
    properties: { id: { type: 'string' } },
  },
  body: {
    type: 'object',
    properties: {
      name: { type: 'string', minLength: 1 },
      description: { type: ['string', 'null'] },
    },
  },
  response: { 200: itemResponse },
};

export const deleteItemSchema: FastifySchema = {
  params: {
    type: 'object',
    required: ['id'],
    properties: { id: { type: 'string' } },
  },
};
