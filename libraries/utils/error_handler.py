import traceback
import functools
def error_handler(func,file_name='error_log.txt'):
    """
    A decorator specifically designed for class methods 
    to preserve the instance method behavior.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None
    
    return wrapper