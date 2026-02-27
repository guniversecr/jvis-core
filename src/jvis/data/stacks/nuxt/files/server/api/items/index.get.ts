import { prisma } from '~/server/utils/prisma';

export default defineEventHandler(async () => {
  return prisma.item.findMany({ orderBy: { createdAt: 'desc' } });
});
