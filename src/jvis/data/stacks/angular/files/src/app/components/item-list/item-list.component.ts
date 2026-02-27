import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { Item } from '../../models/item.model';
import { ItemCardComponent } from '../item-card/item-card.component';

@Component({
  selector: 'app-item-list',
  standalone: true,
  imports: [ItemCardComponent],
  templateUrl: './item-list.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ItemListComponent {
  @Input({ required: true }) items: Item[] = [];
  @Output() deleteItem = new EventEmitter<string>();
}
