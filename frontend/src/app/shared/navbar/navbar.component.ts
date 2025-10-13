import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  @Input() brand = { name: 'EduSpace', href: '/' };

  @Input() links = [
    { label: 'Home', to: '/' },
    { label: 'Features', to: '/features' },
    { label: 'Pricing', to: '/pricing' },
    { label: 'About', to: '/about' }
  ];

  @Input() cta = { label: 'Get Started', to: '/auth' };

  isCollapsed = true;
  toggleMenu() {
    this.isCollapsed = !this.isCollapsed;
  }
}
