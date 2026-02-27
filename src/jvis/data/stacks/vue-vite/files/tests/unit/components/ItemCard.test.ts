import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import ItemCard from '../../../src/components/ui/ItemCard.vue';

describe('ItemCard', () => {
  const item = {
    id: '1',
    name: 'Test Item',
    description: 'A test item',
    createdAt: '2026-01-01T00:00:00Z',
    updatedAt: '2026-01-01T00:00:00Z',
  };

  it('should render item name', () => {
    const wrapper = mount(ItemCard, { props: { item } });
    expect(wrapper.text()).toContain('Test Item');
  });

  it('should render description when present', () => {
    const wrapper = mount(ItemCard, { props: { item } });
    expect(wrapper.text()).toContain('A test item');
  });

  it('should emit delete event when button is clicked', async () => {
    const wrapper = mount(ItemCard, { props: { item } });
    await wrapper.find('button').trigger('click');
    expect(wrapper.emitted('delete')).toBeTruthy();
    expect(wrapper.emitted('delete')![0]).toEqual(['1']);
  });
});
