import { useState } from 'preact/hooks';
import type { CreateItemInput } from '../types/item';

interface Props {
  onSubmit: (input: CreateItemInput) => void;
}

export default function ItemForm({ onSubmit }: Props) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: Event) => {
    e.preventDefault();
    if (!name.trim()) return;
    onSubmit({ name: name.trim(), description: description.trim() || undefined });
    setName('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} class="item-form">
      <input
        value={name}
        onInput={(e) => setName((e.target as HTMLInputElement).value)}
        placeholder="Item name"
        required
      />
      <input
        value={description}
        onInput={(e) => setDescription((e.target as HTMLInputElement).value)}
        placeholder="Description (optional)"
      />
      <button type="submit">Add Item</button>
    </form>
  );
}
