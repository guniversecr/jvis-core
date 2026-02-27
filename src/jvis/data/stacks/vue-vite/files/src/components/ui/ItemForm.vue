<script setup lang="ts">
import { ref } from 'vue';
import type { CreateItemInput } from '../../types/item';

const emit = defineEmits<{ submit: [input: CreateItemInput] }>();

const name = ref('');
const description = ref('');
const submitting = ref(false);

async function handleSubmit() {
  if (!name.value.trim()) return;
  submitting.value = true;
  try {
    emit('submit', {
      name: name.value.trim(),
      description: description.value.trim() || null,
    });
    name.value = '';
    description.value = '';
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="item-form">
    <input v-model="name" type="text" placeholder="Item name" required />
    <input v-model="description" type="text" placeholder="Description (optional)" />
    <button type="submit" :disabled="submitting || !name.trim()">
      {{ submitting ? 'Creating...' : 'Create Item' }}
    </button>
  </form>
</template>
