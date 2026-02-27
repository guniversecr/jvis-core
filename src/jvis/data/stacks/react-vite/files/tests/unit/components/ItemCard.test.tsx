import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ItemCard } from '../../../src/components/ui/ItemCard';

describe('ItemCard', () => {
  const item = {
    id: '1',
    name: 'Test Item',
    description: 'A test item',
    createdAt: '2026-01-01T00:00:00Z',
    updatedAt: '2026-01-01T00:00:00Z',
  };

  it('should render item name', () => {
    render(<ItemCard item={item} onDelete={vi.fn().mockResolvedValue(undefined)} />);
    expect(screen.getByText('Test Item')).toBeInTheDocument();
  });

  it('should render description when present', () => {
    render(<ItemCard item={item} onDelete={vi.fn().mockResolvedValue(undefined)} />);
    expect(screen.getByText('A test item')).toBeInTheDocument();
  });

  it('should call onDelete when delete button is clicked', () => {
    const onDelete = vi.fn().mockResolvedValue(undefined);
    render(<ItemCard item={item} onDelete={onDelete} />);
    fireEvent.click(screen.getByText('Delete'));
    expect(onDelete).toHaveBeenCalledWith('1');
  });
});
