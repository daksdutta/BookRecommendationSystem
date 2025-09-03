import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { BookService } from '../../../core/services/book.service';
@Component({
  selector: 'app-recommendation-page',
  templateUrl: './recommendation-page.component.html',
  styleUrls: ['./recommendation-page.component.css']
})
export class RecommendationPageComponent implements OnInit {
  form!: FormGroup;
  popularBooks: any[] = [];
  recommendations: any[] = [];
  loading = false;
  isSearchMode = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private bookService: BookService
  ) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      book: ['']
    });
    this.loadPopularBooks();
  }

  loadPopularBooks() {
    this.bookService.getPopularBooks().subscribe({
      next: (data: any) => (this.popularBooks = data),
      error: (err) => console.error(err)
    });
  }

  onSubmit() {
    const bookName = this.form.value.book;
    if (!bookName) return;

    this.loading = true;
    this.isSearchMode = true;
    this.recommendations = [];

    this.bookService.getRecommendations(bookName).subscribe({
      next: (data: any) => {
        this.recommendations = data;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
      }
    });
  }

  goHome() {
    this.isSearchMode = false;
    this.recommendations = [];
    this.form.reset();
  }
}
