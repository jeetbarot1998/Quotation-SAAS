from functools import wraps
from typing import Callable
from sqlalchemy.orm import Query
import inspect


def debug_query(func: Callable) -> Callable:
    """
    Decorator to debug SQLAlchemy queries with parameter values.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        query = func(*args, **kwargs)

        if isinstance(query, Query):
            frame = inspect.currentframe()
            calling_frame = frame.f_back
            filename = calling_frame.f_code.co_filename
            lineno = calling_frame.f_lineno

            # Get the compiled query with placeholders
            compiled = query.statement.compile()

            # Get the parameters
            params = compiled.params

            # Print debug information
            print("\n" + "=" * 80)
            print(f"Query Debug at {filename}:{lineno}")
            print("-" * 80)
            print("SQL Query with placeholders:")
            print(str(compiled))
            print("-" * 80)
            print("Parameters:")
            for key, value in params.items():
                print(f"{key}: {value}")
            print("=" * 80)
            print("Final SQL:")
            print(query.statement.compile(compile_kwargs={"literal_binds": True}))
            print("=" * 80 + "\n")

        return query

    return wrapper