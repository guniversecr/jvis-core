<script setup lang="ts">
import { ref } from 'vue';
import type { Item } from '../../types/item';

const props = defineProps<{ item: Item }>();
const emit = defineEmits<{ delete: [id: string] }>();

const deleting = ref(false);

async function handleDelete() {
  deleting.value = true;
  emit('delete', props.item.id);
}
</script>

<template>
  <div class="item-card">
    <h3>{{ item.name }}</h3>
    <p v-if="item.description">{{ item.description }}</p>
    <button type="button" @click="handleDelete" :disabled="deleting">
      {{ deleting ? 'Deleting...' : 'Delete' }}
    </button>
  </div>
</template>
