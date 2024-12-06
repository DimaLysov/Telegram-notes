from .add_handlers.add_person import router_add_person
from .add_handlers.create_family import router_create_family
from .view_handlers.all_family import router_all_family
from .help import router_help
from .start import router_start

routers = [router_add_person,
           router_create_family,
           router_all_family,
           router_help,
           router_start]

