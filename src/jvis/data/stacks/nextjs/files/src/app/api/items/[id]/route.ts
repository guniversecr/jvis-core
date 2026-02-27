import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

interface Params {
  params: { id: string };
}

export async function GET(_request: Request, { params }: Params) {
  const item = await prisma.item.findUnique({ where: { id: params.id } });

  if (!item) {
    return NextResponse.json({ error: 'Item not found' }, { status: 404 });
  }

  return NextResponse.json(item);
}

export async function PATCH(request: Request, { params }: Params) {
  const body = await request.json();

  try {
    const item = await prisma.item.update({
      where: { id: params.id },
      data: {
        ...(body.name !== undefined && { name: body.name }),
        ...(body.description !== undefined && { description: body.description }),
      },
    });
    return NextResponse.json(item);
  } catch {
    return NextResponse.json({ error: 'Item not found' }, { status: 404 });
  }
}

export async function DELETE(_request: Request, { params }: Params) {
  try {
    await prisma.item.delete({ where: { id: params.id } });
    return new NextResponse(null, { status: 204 });
  } catch {
    return NextResponse.json({ error: 'Item not found' }, { status: 404 });
  }
}
