import { createReducer, on } from '@ngrx/store';
import { loginSuccess, logout, setLoading } from './user.actions';
import { User } from './user.model';

export interface UserState {
  user: User | null;
  loading: boolean;
}

export const initialState: UserState = {
  user: null,
  loading: false,
};

export const userReducer = createReducer(
  initialState,
  on(loginSuccess, (state, { user }) => ({ ...state, user })),
  on(logout, (state) => ({ ...state, user: null })),
  on(setLoading, (state, { loading }) => ({ ...state, loading }))
);
