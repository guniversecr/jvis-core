<script lang="ts">
  import type { Item } from '../types/item';
  import { createEventDispatcher } from 'svelte';

  export let item: Item;

  const dispatch = createEventDispatcher<{ delete: string }>();
  let deleting = false;

  function handleDelete() {
    deleting = true;
    dispatch('delete', item.id);
  }
</script>

<div class="item-card">
  <h3>{item.name}</h3>
  {#if item.description}
    <p>{item.description}</p>
  {/if}
  <button type="button" on:click={handleDelete} disabled={deleting}>
    {deleting ? 'Deleting...' : 'Delete'}
  </button>
</div>
