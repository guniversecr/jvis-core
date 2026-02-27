import { prisma } from '~/server/utils/prisma';

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id');

  const item = await prisma.item.findUnique({ where: { id } });

  if (!item) {
    throw createError({ statusCode: 404, message: `Item with id '${id}' not found` });
  }

  return item;
});
