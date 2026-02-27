import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Item, CreateItemInput, UpdateItemInput } from '../models/item.model';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ItemService {
  private readonly baseUrl = `${environment.apiUrl}/items`;

  constructor(private http: HttpClient) {}

  list(): Observable<Item[]> {
    return this.http.get<Item[]>(this.baseUrl);
  }

  get(id: string): Observable<Item> {
    return this.http.get<Item>(`${this.baseUrl}/${id}`);
  }

  create(input: CreateItemInput): Observable<Item> {
    return this.http.post<Item>(this.baseUrl, input);
  }

  update(id: string, input: UpdateItemInput): Observable<Item> {
    return this.http.patch<Item>(`${this.baseUrl}/${id}`, input);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
