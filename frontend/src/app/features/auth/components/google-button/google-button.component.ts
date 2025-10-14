import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-google-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './google-button.component.html',
  styleUrls: ['./google-button.component.css'],
})
export class GoogleButtonComponent {
  loading = false;

  constructor(private auth: AuthService) {}

  loginWithGoogle() {
    window.location.href = this.auth.googleOAuthUrl;
  }
}
