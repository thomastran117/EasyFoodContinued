import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { selectUser } from '../../core/stores/user.selectors';
import { User } from '../../core/stores/user.model';
import { UserState } from '../../core/stores/user.reducer';
import { clearUser } from '../../core/stores/user.actions';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent {
  @Input() brand = { name: 'EasyFood', href: '/' };

  @Input() links = [
    { label: 'Home', to: '/' },
    { label: 'Features', to: '/features' },
    { label: 'Pricing', to: '/pricing' },
    { label: 'About', to: '/about' },
  ];

  @Input() cta = { label: 'Login', to: '/auth/login' };

  user$: Observable<User | null>;
  isCollapsed = true;

  constructor(private store: Store<{ user: UserState }>) {
    this.user$ = this.store.select(selectUser);
  }

  toggleMenu() {
    this.isCollapsed = !this.isCollapsed;
  }

  logout() {
    this.store.dispatch(clearUser());
  }
}
