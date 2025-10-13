import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ProtectedApiService {
  private readonly base = environment.backendUrl;

  constructor(private http: HttpClient) {}

  getProfile() {
    return this.http.get(`${this.base}/user/profile`);
  }

  updateProfile(data: any) {
    return this.http.put(`${this.base}/user/profile`, data);
  }
}
