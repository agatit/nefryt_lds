import React, { Dispatch } from 'react';
import { shallowEqual, useDispatch, useSelector } from 'react-redux';
import { SnackbarKey, useSnackbar } from 'notistack';
import { RootState, store } from '../../app/store';
import { setDisplayedSnackbar } from '../../features/template/templateSlice';

let displayed: any[] = [];

const useNotifier = () => {
    //const dispatch = useDispatch();

    const dispatch: Dispatch<any> = useDispatch();
    //const notifications = useSelector(store => store.tem.notifications || []);
    const notifications = useSelector(
      (state: RootState) => state.template.notifications,
      shallowEqual
    )

    const { enqueueSnackbar, closeSnackbar } = useSnackbar();

    const storeDisplayed = (id: any) => {
        displayed = [...displayed, id];
    };

    const removeDisplayed = (id: SnackbarKey) => {
        displayed = [...displayed.filter(key => id !== key)];
    };

    React.useEffect(() => {
       // console.log(notifications);
        notifications.forEach(({ key, message, options = {}, dismissed = false }) => {
            dispatch(setDisplayedSnackbar(key));
            if (dismissed) {
                // dismiss snackbar using notistack
                closeSnackbar(key);
                return;
            }

            // do nothing if snackbar is already displayed
            if (displayed.includes(key)) return;

            
            // display snackbar using notistack
            enqueueSnackbar(message, {
                key,
                ...options,
                onClose: (event, reason, myKey) => {
                    
                },
                onExited: (event, myKey) => {
                    // remove this snackbar from redux store
                    removeDisplayed(myKey);
                },
            });

            // keep track of snackbars that we've displayed
            storeDisplayed(key);
        });
    }, [notifications, closeSnackbar, enqueueSnackbar, dispatch]);
};

export default useNotifier;
