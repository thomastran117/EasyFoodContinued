import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { SessionManagerService } from './core/services/session-manager.service';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, NgIf],
  templateUrl: './app.html',
})
export class App implements OnInit {
  private session = inject(SessionManagerService);
  protected readonly title = 'frontend';

  ngOnInit(): void {
    this.session.restoreSession();
  }

  get loading() {
    return this.session.loading();
  }
}
