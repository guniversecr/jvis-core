import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { ItemService } from './item.service';
import { Item } from '../models/item.model';
import { environment } from '../../environments/environment';

describe('ItemService', () => {
  let service: ItemService;
  let httpTesting: HttpTestingController;
  const baseUrl = `${environment.apiUrl}/items`;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ItemService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('should list items', () => {
    const mockItems: Item[] = [
      { id: '1', name: 'Item 1', description: null, createdAt: '', updatedAt: '' },
    ];

    service.list().subscribe((items) => {
      expect(items).toEqual(mockItems);
    });

    const req = httpTesting.expectOne(baseUrl);
    expect(req.request.method).toBe('GET');
    req.flush(mockItems);
  });

  it('should create an item', () => {
    const mockItem: Item = { id: '1', name: 'New', description: null, createdAt: '', updatedAt: '' };

    service.create({ name: 'New' }).subscribe((item) => {
      expect(item).toEqual(mockItem);
    });

    const req = httpTesting.expectOne(baseUrl);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ name: 'New' });
    req.flush(mockItem);
  });

  it('should delete an item', () => {
    service.delete('1').subscribe();

    const req = httpTesting.expectOne(`${baseUrl}/1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
