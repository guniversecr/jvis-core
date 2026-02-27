<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { CreateItemInput } from '../types/item';

  const dispatch = createEventDispatcher<{ submit: CreateItemInput }>();
  let name = '';
  let description = '';
  let submitting = false;

  async function handleSubmit() {
    if (!name.trim()) return;
    submitting = true;
    try {
      dispatch('submit', {
        name: name.trim(),
        description: description.trim() || null,
      });
      name = '';
      description = '';
    } finally {
      submitting = false;
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="item-form">
  <input type="text" placeholder="Item name" bind:value={name} required />
  <input type="text" placeholder="Description (optional)" bind:value={description} />
  <button type="submit" disabled={submitting || !name.trim()}>
    {submitting ? 'Creating...' : 'Create Item'}
  </button>
</form>
