import toast from 'react-hot-toast';

export const showToast = {
  success: (message: string) => toast.success(message),
  error: (message: string) => toast.error(message),
  warning: (message: string) => toast(message, { icon: '⚠️' }),
  info: (message: string) => toast(message, { icon: 'ℹ️' }),
};

export default showToast;