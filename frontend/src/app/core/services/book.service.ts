import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  getPopularBooks(): Observable<any> {
    return this.http.get(`${this.baseUrl}/popular`);
  }

  getRecommendations(book: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/recommend?book=${book}`);
  }
}
