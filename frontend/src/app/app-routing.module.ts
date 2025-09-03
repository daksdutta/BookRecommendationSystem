import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecommendationPageComponent } from './features/pages/recommendation-page/recommendation-page.component';
import { SearchComponent } from './features/pages/search/search.component';
const routes: Routes = [
  { path: '', component: RecommendationPageComponent },            // Popular books
  { path: 'search/:book', component: SearchComponent }, // Recommendations
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
