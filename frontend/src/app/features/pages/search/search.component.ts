import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BookService } from '../../../core/services/book.service';
@Component({
  selector: 'app-search',
  templateUrl: './search.component.html'
})
export class SearchComponent implements OnInit {
  bookName = '';
  recommendations: any[] = [];
  loading = false;
  errorMsg = '';

  constructor(private route: ActivatedRoute, private bookService: BookService) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.bookName = params['book'];
      this.fetchRecommendations();
    });
  }

  fetchRecommendations() {
    this.loading = true;
    this.errorMsg = '';
    this.recommendations = [];

    this.bookService.getRecommendations(this.bookName).subscribe({
      next: (data) => {
        this.recommendations = data;
        this.loading = false;
      },
      error: () => {
        this.errorMsg = `No recommendations found for "${this.bookName}"`;
        this.loading = false;
      }
    });
  }
}
