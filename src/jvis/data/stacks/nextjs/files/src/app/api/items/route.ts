import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export async function GET() {
  const items = await prisma.item.findMany({ orderBy: { createdAt: 'desc' } });
  return NextResponse.json(items);
}

export async function POST(request: Request) {
  const body = await request.json();

  if (!body.name || typeof body.name !== 'string') {
    return NextResponse.json({ error: 'name is required' }, { status: 400 });
  }

  const item = await prisma.item.create({
    data: {
      name: body.name,
      description: body.description ?? null,
    },
  });

  return NextResponse.json(item, { status: 201 });
}
