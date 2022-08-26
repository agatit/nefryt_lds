// Or from '@reduxjs/toolkit/query' if not using the auto-generated hooks
import { RootState } from "..";
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

// initialize an empty api service that we'll inject endpoints into later as needed
export const api = createApi({
  baseQuery: fetchBaseQuery({ 
    baseUrl: '/',
    mode: 'cors',
    prepareHeaders: (headers, { getState }) => {
      // By default, if we have a token in the store, let's use that for authenticated requests
      const token = (getState() as RootState).auth.token
      if (token) {
        headers.set('authentication', `Bearer ${token}`)
      }
      return headers
    }, 
  }),
  endpoints: () => ({}), 
})