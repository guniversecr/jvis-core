<script lang="ts">
  import type { Item } from '../types/item';
  import ItemCard from './ItemCard.svelte';
  import { createEventDispatcher } from 'svelte';

  export let items: Item[];
  const dispatch = createEventDispatcher<{ delete: string }>();
</script>

{#if items.length === 0}
  <p>No items yet. Create one above.</p>
{:else}
  <ul class="item-list">
    {#each items as item (item.id)}
      <li>
        <ItemCard {item} on:delete />
      </li>
    {/each}
  </ul>
{/if}
