from .add_handlers.add_person_hd import router_add_person
from .add_handlers.create_family_hd import router_create_family
from .choose_handlers.choose_family_hd import router_choose_family
from .view_handlers.all_family_hd import router_all_family
from .help_hd import router_help
from .start_hd import router_start

routers = [router_add_person,
           router_create_family,
           router_choose_family,
           router_all_family,
           router_help,
           router_start]

