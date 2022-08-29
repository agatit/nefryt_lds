import { createSlice } from '@reduxjs/toolkit'

export const templateSlice = createSlice({
  name: 'template',
  initialState: {
    sidebar_open: false,
  },
  reducers: {
    toggleSidebar: (state) => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.sidebar_open = !state.sidebar_open;
    },
    
  },
})

export const { toggleSidebar } = templateSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default templateSlice.reducer
