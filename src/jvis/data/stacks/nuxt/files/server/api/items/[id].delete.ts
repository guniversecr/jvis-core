import { prisma } from '~/server/utils/prisma';

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id');

  const existing = await prisma.item.findUnique({ where: { id } });

  if (!existing) {
    throw createError({ statusCode: 404, message: `Item with id '${id}' not found` });
  }

  await prisma.item.delete({ where: { id } });

  setResponseStatus(event, 204);
  return null;
});
