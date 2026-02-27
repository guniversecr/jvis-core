<script setup lang="ts">
import type { Item } from '../../types/item';
import ItemCard from './ItemCard.vue';

defineProps<{ items: Item[] }>();
const emit = defineEmits<{ delete: [id: string] }>();
</script>

<template>
  <p v-if="items.length === 0">No items yet. Create one above.</p>
  <ul v-else class="item-list">
    <li v-for="item in items" :key="item.id">
      <ItemCard :item="item" @delete="emit('delete', $event)" />
    </li>
  </ul>
</template>
