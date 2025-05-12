from fastapi_cache import KeyBuilder
from fastapi_cache.decorator import cache
from typing import Optional, Union, Any, Awaitable, Dict, Tuple
from fastapi import Response, Request


class SlugKeyBuilder(KeyBuilder):
    def __call__(
            self,
            func: Any,
            namespace: str = "",
            *,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
            args: Tuple[Any, ...],
            kwargs: Dict[str, Any],
    ) -> Union[Awaitable[str], str]:
        # Если в kwargs есть slug, используем его для ключа
        if 'slug' in kwargs:
            return f"{namespace}:{kwargs['slug']}"

        # Если slug передается как часть пути (args)
        # Проверяем позиционные аргументы (обычно для path параметров)
        if args and len(args) > 0:
            # Предполагаем, что slug - первый аргумент после self
            return f"{namespace}:{args[0]}"

        # Если slug не найден, используем стандартный ключ
        return f"{namespace}:default"

