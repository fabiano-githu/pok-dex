
from django.urls import path

from . import views


urlpatterns = [

    # Página inicial
    path(
        "",
        views.home,
        name="home"
    ),

    # Listar Pokémon
    path(
        "pokemon/",
        views.listar_pokemon,
        name="listar_pokemon"
    ),

    # Detalhes do Pokémon
    path(
        "pokemon/<int:id>/",
        views.detalhes,
        name="detalhes"
    ),

    # Cadastrar Pokémon
    path(
        "pokemon/criar/",
        views.criar_pokemon,
        name="criar_pokemon"
    ),

    # Editar Pokémon
    path(
        "pokemon/<int:id>/editar/",
        views.editar_pokemon,
        name="editar_pokemon"
    ),

    # Deletar Pokémon
    path(
        "pokemon/<int:id>/deletar/",
        views.deletar_pokemon,
        name="deletar_pokemon"
    ),
]

