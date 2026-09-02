from django.urls import path

from . import views


urlpatterns = [

    # ==========================================================
    # PÁGINA INICIAL
    # ==========================================================

    path(
        "",
        views.home,
        name="home"
    ),

    # ==========================================================
    # CADASTRAR POKÉMON
    # ==========================================================

    path(
        "pokemon/criar/",
        views.criar_pokemon,
        name="criar_pokemon"
    ),

    # ==========================================================
    # EDITAR POKÉMON
    # ==========================================================

    path(
        "pokemon/<int:id>/editar/",
        views.editar_pokemon,
        name="editar_pokemon"
    ),

    # ==========================================================
    # DELETAR POKÉMON
    # ==========================================================

    path(
        "pokemon/<int:id>/deletar/",
        views.deletar_pokemon,
        name="deletar_pokemon"
    ),

    # ==========================================================
    # LISTAR POKÉMON
    # ==========================================================

    path(
        "pokemon/",
        views.listar_pokemon,
        name="listar_pokemon"
    ),

    # ==========================================================
    # DETALHES DO POKÉMON
    # ==========================================================

    path(
        "pokemon/<int:id>/",
        views.detalhes,
        name="detalhes"
    ),
]