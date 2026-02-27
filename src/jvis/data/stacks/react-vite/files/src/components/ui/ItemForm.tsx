import { useState } from 'react';
import type { CreateItemInput } from '../../types/item';

interface ItemFormProps {
  onSubmit: (input: CreateItemInput) => Promise<unknown>;
}

export function ItemForm({ onSubmit }: ItemFormProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setSubmitting(true);
    try {
      await onSubmit({ name: name.trim(), description: description.trim() || null });
      setName('');
      setDescription('');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="item-form">
      <input
        type="text"
        placeholder="Item name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button type="submit" disabled={submitting || !name.trim()}>
        {submitting ? 'Creating...' : 'Create Item'}
      </button>
    </form>
  );
}
