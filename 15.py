from datetime import datetime, timedelta


# Admin access only
def is_admin(func):
    def wrapper(*args, **kwargs):
        user_type = kwargs.get('user_type')
        if user_type != 'admin':
            raise ValueError("Permission denied.")
        return func(*args, **kwargs)
    return wrapper


@is_admin
def show_customer_receipt(user_type: str):
    print(f'A dangerous operation is performed by the {user_type}.')


try:
    show_customer_receipt(user_type='user')
except Exception as e:
    print(e)

show_customer_receipt(user_type='admin')


# Try-except error printer
def catch_errors(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Found an error during execution of your function.\
 {type(e).__name__}: {str(e)}.")
    return wrapper


@catch_errors
def some_function_with_risky_operation(data):
    print(data['key'])


some_function_with_risky_operation({'foo': 'bar'})
some_function_with_risky_operation({'key': 'bar'})


# Type validation decorator
def check_types(func):
    def wrapper(*args, **kwargs):
        params = func.__annotations__
        # {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

        for v_name, v_value in zip(params.keys(), args):
            if v_name in params and not isinstance(v_value, params[v_name]):
                raise TypeError(f"Argument {v_name} must be\
 {params[v_name].__name__}, not {type(v_value).__name__}.")

        for v_name, v_value in kwargs.items():
            if v_name in params and not isinstance(v_value, params[v_name]):
                raise TypeError(f"Argument {v_name} must be\
 {params[v_name].__name__}, not {type(v_value).__name__}.")

        result = func(*args, **kwargs)

        if 'return' in params and not isinstance(result, params['return']):
            raise TypeError(f"Return value must be\
 {params['return'].__name__}, not {type(result).__name__}.")

        return result
    return wrapper


@check_types
def add(a: int, b: int) -> int:
    return a + b


print(add(1, 2))

try:
    print(add("1", "2"))
except TypeError as e:
    print(e)


# A function result cache system
def cache_results(func):
    cache = {}

    def wrapper(*args, **kwargs):
        key = args + tuple(kwargs[value] for value in sorted(kwargs))
        # print(key)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        # print(cache)
        return cache[key]

    return wrapper


@cache_results
def add_values(first_value: str,
               second_value: str = '2',
               third_value: str = '3') -> str:
    return first_value + second_value + third_value


s1 = add_values('2', '5', '3')
print(id(s1))

s4 = add_values('2', '5', third_value='3')
print(id(s4))

s2 = add_values('2', third_value='3', second_value='5')
print(id(s2))

s3 = add_values('2', second_value='5', third_value='3')
print(id(s3))

s5 = add_values('2', '5')
print(id(s5))


# Executing a function a certain number of times per minute
def rate_limiter(max_calls=100):
    def decorator(func):
        state = {'last_time': datetime.now(), 'calls_made': 0}

        def wrapper(*args, **kwargs):
            current_time = datetime.now()
            last_time = state['last_time']
            calls_made = state['calls_made']

            if current_time - last_time > timedelta(seconds=60):
                state['last_time'] = current_time
                state['calls_made'] = 0

            if calls_made < max_calls:
                state['calls_made'] += 1
                return func(*args, **kwargs)
            else:
                remaining_time = (last_time + timedelta(seconds=60) -
                                  current_time).total_seconds()
                print(f"Rate limit exceeded.\
 Try again in {remaining_time:.2f} seconds.")

        return wrapper

    return decorator


@rate_limiter(max_calls=2)
def function():
    print("Execution of function")


for _ in range(8):
    function()
    import time
    time.sleep(1)
