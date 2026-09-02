import requests

from django import forms
from django.shortcuts import render, redirect, get_object_or_404

from .models import Pokemon

from deep_translator import GoogleTranslator


# ==========================================================
# FORMULÁRIO DO POKÉMON
# ==========================================================

class PokemonForm(forms.ModelForm):

    class Meta:
        model = Pokemon

        fields = [
            "name",
            "species",
            "height",
            "weight",
            "types",
            "abilities",
            "image",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome do Pokémon"
                }
            ),

            "species": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Espécie"
                }
            ),

            "height": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                    "min": "0",
                    "placeholder": "Altura em metros"
                }
            ),

            "weight": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                    "min": "0",
                    "placeholder": "Peso em kg"
                }
            ),

            "types": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Fire, Flying"
                }
            ),

            "abilities": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Blaze, Solar Power"
                }
            ),

            "image": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "URL da imagem"
                }
            ),
        }


# ==========================================================
# SERIALIZAR DADOS DO BANCO
# ==========================================================

def serialize_db_pokemon(pokemon):

    types = [
        value.strip().title()
        for value in pokemon.types.split(",")
        if value.strip()
    ]

    abilities = [
        value.strip().title()
        for value in pokemon.abilities.split(",")
        if value.strip()
    ]

    return {
        "id": pokemon.id,
        "name": pokemon.name,
        "species": pokemon.species,
        "height": pokemon.height,
        "weight": pokemon.weight,
        "types": types,
        "abilities": abilities,
        "image": pokemon.image,
    }


# ==========================================================
# HOME
# ==========================================================

def home(request):

    url = "https://pokeapi.co/api/v2/pokemon?limit=20"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException:

        return render(
            request,
            "home.html",
            {
                "pokemons": [],
                "erro": "Não foi possível acessar a PokéAPI."
            }
        )

    pokemons = []

    for item in data.get("results", []):

        try:

            # ==================================================
            # DADOS PRINCIPAIS
            # ==================================================

            detail_response = requests.get(
                item["url"],
                timeout=10
            )

            detail_response.raise_for_status()

            detail = detail_response.json()

            # ==================================================
            # DADOS DA ESPÉCIE
            # ==================================================

            species_response = requests.get(
                detail["species"]["url"],
                timeout=10
            )

            species_response.raise_for_status()

            species = species_response.json()

            # ==================================================
            # DESCRIÇÃO
            # ==================================================

            descricao = ""

            # Primeiro tenta português
            for texto in species.get(
                "flavor_text_entries",
                []
            ):

                if texto["language"]["name"] == "pt":

                    descricao = texto["flavor_text"]

                    break

            # Se não encontrou português,
            # tenta inglês
            if not descricao:

                for texto in species.get(
                    "flavor_text_entries",
                    []
                ):

                    if texto["language"]["name"] == "en":

                        descricao = texto["flavor_text"]

                        break

            # ==================================================
            # LIMPAR DESCRIÇÃO
            # ==================================================

            descricao = (
                descricao
                .replace("\n", " ")
                .replace("\f", " ")
                .strip()
            )

            # ==================================================
            # TRADUZIR
            # ==================================================

            if descricao:

                try:

                    descricao = GoogleTranslator(
                        source="auto",
                        target="pt"
                    ).translate(descricao)

                except Exception:

                    pass

            # ==================================================
            # TIPOS
            # ==================================================

            tipos = [

                tipo["type"]["name"]
                .replace("-", " ")
                .title()

                for tipo in detail.get(
                    "types",
                    []
                )
            ]

            # ==================================================
            # HABILIDADES
            # ==================================================

            habilidades = [

                habilidade["ability"]["name"]
                .replace("-", " ")
                .title()

                for habilidade in detail.get(
                    "abilities",
                    []
                )
            ]

            # ==================================================
            # IMAGEM
            # ==================================================

            imagem = (
                detail
                .get("sprites", {})
                .get("other", {})
                .get("official-artwork", {})
                .get("front_default")
            )

            # ==================================================
            # DADOS DO POKÉMON
            # ==================================================

            pokemon_data = {

                "nome": detail["name"].capitalize(),

                "imagem": imagem,

                "id": detail["id"],

                "descricao": descricao,

                "peso": detail["weight"] / 10,

                "altura": detail["height"] / 10,

                "tipos": tipos,

                "habilidades": habilidades,
            }

            pokemons.append(
                pokemon_data
            )

        except (
            requests.RequestException,
            KeyError,
            TypeError
        ):

            # Se um Pokémon específico
            # apresentar erro, continua o loop
            continue

    # ==========================================================
    # RENDERIZAR HOME
    # ==========================================================

    return render(
        request,
        "home.html",
        {
            "pokemons": pokemons
        }
    )


# ==========================================================
# DETALHES DO POKÉMON
# ==========================================================

def detalhes(request, id):

    url = f"https://pokeapi.co/api/v2/pokemon/{id}"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        detail = response.json()

    except requests.RequestException:

        return render(
            request,
            "detalhes.html",
            {
                "pokemon": None,
                "erro": "Não foi possível carregar o Pokémon."
            }
        )

    # ======================================================
    # TIPOS
    # ======================================================

    tipos = [

        tipo["type"]["name"]
        .replace("-", " ")
        .title()

        for tipo in detail.get(
            "types",
            []
        )
    ]

    # ======================================================
    # HABILIDADES
    # ======================================================

    habilidades = [

        habilidade["ability"]["name"]
        .replace("-", " ")
        .title()

        for habilidade in detail.get(
            "abilities",
            []
        )
    ]

    # ======================================================
    # SPRITES
    # ======================================================

    sprites = detail.get(
        "sprites",
        {}
    )

    # ======================================================
    # IMAGEM OFICIAL
    # ======================================================

    imagem = (
        sprites
        .get("other", {})
        .get("official-artwork", {})
        .get("front_default")
    )

    # ======================================================
    # DADOS DO POKÉMON
    # ======================================================

    pokemon_data = {

        "id": detail["id"],

        "nome": detail["name"].capitalize(),

        "imagem": imagem,

        "imagem_front": sprites.get(
            "front_default"
        ),

        "imagem_back": sprites.get(
            "back_default"
        ),

        "peso": detail["weight"] / 10,

        "altura": detail["height"] / 10,

        "tipos": tipos,

        "habilidades": habilidades,
    }

    # ======================================================
    # RENDERIZAR
    # ======================================================

    return render(
        request,
        "detalhes.html",
        {
            "pokemon": pokemon_data
        }
    )


# ==========================================================
# CRIAR POKÉMON
# ==========================================================

def criar_pokemon(request):

    if request.method == "POST":

        form = PokemonForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect("home")

    else:

        form = PokemonForm()

    return render(
        request,
        "cadastro.pokemon.html",
        {
            "form": form
        }
    )


# ==========================================================
# EDITAR POKÉMON
# ==========================================================

def editar_pokemon(request, id):

    pokemon = get_object_or_404(
        Pokemon,
        id=id
    )

    if request.method == "POST":

        form = PokemonForm(
            request.POST,
            instance=pokemon
        )

        if form.is_valid():

            form.save()

            return redirect("listar_pokemon")

    else:

        form = PokemonForm(
            instance=pokemon
        )

    return render(
        request,
        "cadastro.pokemon.html",
        {
            "form": form,
            "pokemon": pokemon
        }
    )


# ==========================================================
# DELETAR POKÉMON
# ==========================================================

def deletar_pokemon(request, id):

    pokemon = get_object_or_404(
        Pokemon,
        id=id
    )

    if request.method == "POST":

        pokemon.delete()

        return redirect("listar_pokemon")

    return render(
        request,
        "confirmar_exclusao.html",
        {
            "pokemon": pokemon
        }
    )


# ==========================================================
# LISTAR POKÉMON DO BANCO
# ==========================================================

def listar_pokemon(request):

    pokemons = Pokemon.objects.all()

    return render(
        request,
        "home.html",
        {
            "pokemons": pokemons
        }
    )