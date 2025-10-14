import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-microsoft-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './microsoft-button.component.html',
  styleUrls: ['./microsoft-button.component.css'],
})
export class MicrosoftButtonComponent {
  loading = false;

  constructor(private auth: AuthService) {}

  loginWithMicrosoft() {
    window.location.href = this.auth.microsoftOAuthUrl;
  }
}
