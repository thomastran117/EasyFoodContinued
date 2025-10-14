import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { LoginComponent } from './pages/login/login.component';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    LoginComponent,
    RouterModule.forChild([
      { path: 'login', component: LoginComponent },
    ]),
  ],
})
export class AuthModule {}
