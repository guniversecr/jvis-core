<script setup lang="ts">
import { useItems } from '../composables/useItems';
import ItemList from '../components/ui/ItemList.vue';
import ItemForm from '../components/ui/ItemForm.vue';

const { items, loading, error, createItem, deleteItem } = useItems();
</script>

<template>
  <div>
    <h2>Items</h2>
    <ItemForm @submit="createItem" />
    <p v-if="error" class="error-message">{{ error }}</p>
    <p v-if="loading">Loading...</p>
    <ItemList v-else :items="items" @delete="deleteItem" />
  </div>
</template>
