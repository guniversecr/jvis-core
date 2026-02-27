import { prisma } from '~/server/utils/prisma';

export default defineEventHandler(async (event) => {
  const body = await readBody(event);

  if (!body.name || typeof body.name !== 'string' || body.name.trim() === '') {
    throw createError({ statusCode: 400, message: 'name is required' });
  }

  const item = await prisma.item.create({
    data: {
      name: body.name.trim(),
      description: body.description ?? null,
    },
  });

  setResponseStatus(event, 201);
  return item;
});
