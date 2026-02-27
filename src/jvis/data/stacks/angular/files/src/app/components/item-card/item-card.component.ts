import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { Item } from '../../models/item.model';

@Component({
  selector: 'app-item-card',
  standalone: true,
  templateUrl: './item-card.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ItemCardComponent {
  @Input({ required: true }) item!: Item;
  @Output() deleteItem = new EventEmitter<string>();

  onDelete(): void {
    this.deleteItem.emit(this.item.id);
  }
}
