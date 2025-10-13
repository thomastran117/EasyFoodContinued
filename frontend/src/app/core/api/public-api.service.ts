import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PublicApiService {
  private readonly base = environment.backendUrl;

  constructor(private http: HttpClient) {}

  login(payload: { email: string; password: string }) {
    return this.http.post(`${this.base}/auth/login`, payload);
  }

  signup(payload: any) {
    return this.http.post(`${this.base}/auth/signup`, payload);
  }

  getPublicContent() {
    return this.http.get(`${this.base}/public`);
  }
}
