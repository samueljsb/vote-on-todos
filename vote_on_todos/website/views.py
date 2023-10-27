from __future__ import annotations

from typing import Any

from django.views import generic

from . import config


class Lists(generic.TemplateView):
    template_name = 'lists.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        queries = config.get_list_queries()

        context = {
            'todo_lists': sorted(
                queries.get_lists(), key=lambda lst: lst.name,
            ),
        }

        return context
