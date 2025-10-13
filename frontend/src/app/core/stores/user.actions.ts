import { createAction, props } from '@ngrx/store';
import { User } from './user.model';

export const loginSuccess = createAction('[User] Login Success', props<{ user: User }>());
export const logout = createAction('[User] Logout');
export const setLoading = createAction('[User] Set Loading', props<{ loading: boolean }>());
