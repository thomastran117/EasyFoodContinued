import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

interface TokenResponse {
  accessToken: string;
  refreshToken: string;
}

@Injectable({ providedIn: 'root' })
export class AuthTokenService {
  private accessKey = 'access_token';
  private refreshKey = 'refresh_token';

  constructor(private http: HttpClient) {}

  get accessToken(): string | null {
    return localStorage.getItem(this.accessKey);
  }

  get refreshToken(): string | null {
    return localStorage.getItem(this.refreshKey);
  }

  setTokens(access: string, refresh: string) {
    localStorage.setItem(this.accessKey, access);
    localStorage.setItem(this.refreshKey, refresh);
  }

  clearTokens() {
    localStorage.removeItem(this.accessKey);
    localStorage.removeItem(this.refreshKey);
  }

  async refresh(): Promise<void> {
    if (!this.refreshToken) throw new Error('Missing refresh token');
    const res = await this.http
      .post<TokenResponse>(`${environment.backendUrl}/auth/refresh`, {
        refreshToken: this.refreshToken,
      })
      .toPromise();
    this.setTokens(res!.accessToken, res!.refreshToken);
  }
}
