import { Component, OnInit, ChangeDetectionStrategy, signal } from '@angular/core';
import { ItemFormComponent } from '../../components/item-form/item-form.component';
import { ItemListComponent } from '../../components/item-list/item-list.component';
import { ItemService } from '../../services/item.service';
import { Item, CreateItemInput } from '../../models/item.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ItemFormComponent, ItemListComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomeComponent implements OnInit {
  items = signal<Item[]>([]);
  error = signal<string | null>(null);

  constructor(private itemService: ItemService) {}

  ngOnInit(): void {
    this.loadItems();
  }

  loadItems(): void {
    this.itemService.list().subscribe({
      next: (items) => this.items.set(items),
      error: (err) => this.error.set(err.message || 'Failed to load items'),
    });
  }

  onAddItem(input: CreateItemInput): void {
    this.itemService.create(input).subscribe({
      next: () => this.loadItems(),
      error: (err) => this.error.set(err.message || 'Failed to create item'),
    });
  }

  onDeleteItem(id: string): void {
    this.itemService.delete(id).subscribe({
      next: () => this.loadItems(),
      error: (err) => this.error.set(err.message || 'Failed to delete item'),
    });
  }
}
