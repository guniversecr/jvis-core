import { prisma } from '~/server/utils/prisma';

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id');
  const body = await readBody(event);

  const existing = await prisma.item.findUnique({ where: { id } });

  if (!existing) {
    throw createError({ statusCode: 404, message: `Item with id '${id}' not found` });
  }

  return prisma.item.update({
    where: { id },
    data: {
      ...(body.name !== undefined && { name: body.name }),
      ...(body.description !== undefined && { description: body.description }),
    },
  });
});
