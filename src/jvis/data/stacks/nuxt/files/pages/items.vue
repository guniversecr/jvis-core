<script setup lang="ts">
const { items, loading, error, fetchItems, createItem, deleteItem } = useItems();

const newName = ref('');
const newDescription = ref('');
const submitting = ref(false);

async function handleSubmit() {
  if (!newName.value.trim()) return;
  submitting.value = true;
  try {
    await createItem({
      name: newName.value.trim(),
      description: newDescription.value.trim() || null,
    });
    newName.value = '';
    newDescription.value = '';
  } finally {
    submitting.value = false;
  }
}

onMounted(fetchItems);
</script>

<template>
  <div>
    <h2>Items</h2>

    <form @submit.prevent="handleSubmit" class="item-form">
      <input v-model="newName" type="text" placeholder="Item name" required />
      <input v-model="newDescription" type="text" placeholder="Description (optional)" />
      <button type="submit" :disabled="submitting || !newName.trim()">
        {{ submitting ? 'Creating...' : 'Create Item' }}
      </button>
    </form>

    <p v-if="error" class="error-message">{{ error }}</p>
    <p v-if="loading">Loading...</p>

    <ul v-else-if="items.length" class="item-list">
      <li v-for="item in items" :key="item.id" class="item-card">
        <h3>{{ item.name }}</h3>
        <p v-if="item.description">{{ item.description }}</p>
        <button @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>

    <p v-else>No items yet. Create one above.</p>
  </div>
</template>
