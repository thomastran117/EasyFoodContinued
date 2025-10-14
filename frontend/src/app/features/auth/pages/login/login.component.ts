import { Component } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Store } from '@ngrx/store';
import { AuthService } from '../../services/auth.service';
import { setUser } from '../../../../core/stores/user.actions';
import { UserState } from '../../../../core/stores/user.reducer';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { GoogleButtonComponent } from '../../components/google-button/google-button.component';
import { MicrosoftButtonComponent } from '../../components/microsoft-button/microsoft-button.component';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    GoogleButtonComponent,
    MicrosoftButtonComponent,
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  loading = false;
  error = '';
  submitted = false;
  showPw = false;
  form!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private store: Store<{ user: UserState }>,
    private router: Router,
  ) {}

  ngOnInit() {
    this.form = this.fb.nonNullable.group({
      email: this.fb.nonNullable.control('', [Validators.required, Validators.email]),
      password: this.fb.nonNullable.control('', [Validators.required, Validators.minLength(6)]),
      remember: this.fb.nonNullable.control(false),
    });
  }

  togglePassword() {
    this.showPw = !this.showPw;
  }

  onSubmit() {
    this.submitted = true;
    if (this.form.invalid) return;

    this.loading = true;
    this.error = '';

    this.auth
      .login(this.form.value)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: (res) => {
          this.store.dispatch(setUser({ user: res }));
          this.router.navigate(['/dashboard']);
        },
        error: (err) => {
          console.error('Login failed:', err);
          this.error = err?.error?.message || 'Login failed.';
        },
      });
  }
}
