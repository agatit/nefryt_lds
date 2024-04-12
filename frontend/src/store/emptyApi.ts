// Or from '@reduxjs/toolkit/query' if not using the auto-generated hooks
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { AuthData, selectIsAuthenticated } from '../features/auth/authSlice'
import { RootState } from '../app/store';



// initialize an empty api service that we'll inject endpoints into later as needed
export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:8080/',
  prepareHeaders: (headers, { getState }) => {
      var token = localStorage.getItem('token');
      headers.set('Access-Control-Allow-Origin', '*')
      headers.set('Authorization', `Bearer ${token}`)
    return headers}
  
  }),
  
  endpoints: () => ({}),
})

