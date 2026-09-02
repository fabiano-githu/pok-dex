
import requests

from django import forms
from django.shortcuts import render

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
                    "class": "form-control"
                }
            ),

            "species": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "height": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                    "min": "0"
                }
            ),

            "weight": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                    "min": "0"
                }
            ),

            "types": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "abilities": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "image": forms.URLInput(
                attrs={
                    "class": "form-control"
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
        "types": types,
        "abilities": abilities,
    }


# ==========================================================
# HOME
# ==========================================================

def home(request):

    url = "https://pokeapi.co/api/v2/pokemon?limit=20"

    response = requests.get(url)

    data = response.json()

    pokemons = []

    for item in data["results"]:

        # ==================================================
        # DADOS PRINCIPAIS
        # ==================================================

        detail_response = requests.get(item["url"])

        detail = detail_response.json()

        # ==================================================
        # DADOS DA ESPÉCIE
        # ==================================================

        species_response = requests.get(
            detail["species"]["url"]
        )

        species = species_response.json()

        # ==================================================
        # BUSCAR DESCRIÇÃO
        # ==================================================

        descricao = ""

        # Primeiro tenta português
        for texto in species["flavor_text_entries"]:

            if texto["language"]["name"] == "pt":

                descricao = texto["flavor_text"]

                break

        # Se não encontrou português,
        # pega inglês
        if not descricao:

            for texto in species["flavor_text_entries"]:

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
        )

        # ==================================================
        # TRADUZIR PARA PORTUGUÊS
        # ==================================================

        if descricao:

            try:

                descricao = GoogleTranslator(
                    source="auto",
                    target="pt"
                ).translate(descricao)

            except Exception:

                # Se a tradução falhar,
                # mantém a descrição original
                pass

        # ==================================================
        # TIPOS
        # ==================================================

        tipos = [
            tipo["type"]["name"].capitalize()
            for tipo in detail["types"]
        ]

        # ==================================================
        # HABILIDADES
        # ==================================================

        habilidades = [
            habilidade["ability"]["name"].replace("-", " ").title()
            for habilidade in detail["abilities"]
        ]

        # ==================================================
        # CRIAR OBJETO DO POKÉMON
        # ==================================================

        pokemon_data = {

            "nome": detail["name"].capitalize(),

            "imagem": (
                detail["sprites"]
                ["other"]
                ["official-artwork"]
                ["front_default"]
            ),

            "id": detail["id"],

            "descricao": descricao,

            "peso": detail["weight"] / 10,

            "altura": detail["height"] / 10,

            "tipos": tipos,

            "habilidades": habilidades,
        }

        pokemons.append(pokemon_data)

    # ======================================================
    # RENDERIZAR HOME
    # ======================================================

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

    response = requests.get(url)

    detail = response.json()

    # ======================================================
    # TIPOS
    # ======================================================

    tipos = [
        tipo["type"]["name"].capitalize()
        for tipo in detail["types"]
    ]

    # ======================================================
    # HABILIDADES
    # ======================================================

    habilidades = [
        habilidade["ability"]["name"].replace("-", " ").title()
        for habilidade in detail["abilities"]
    ]

    # ======================================================
    # OBJETO DO POKÉMON
    # ======================================================

    pokemon_data = {

        "id": detail["id"],

        "nome": detail["name"].capitalize(),

        "imagem": (
            detail["sprites"]
            ["other"]
            ["official-artwork"]
            ["front_default"]
        ),

        "imagem_front": detail["sprites"]["front_default"],

        "imagem_back": detail["sprites"]["back_default"],

        "peso": detail["weight"] / 10,

        "altura": detail["height"] / 10,

        "tipos": tipos,

        "habilidades": habilidades,
    }

    # ======================================================
    # RENDERIZAR DETALHES
    # ======================================================

    return render(
        request,
        "detalhes.html",
        {
            "pokemon": pokemon_data
        }
    )

# ======================================================
    # criar pokemon no form
    # ======================================================


def criar_pokemon(request):

    if request.method == "POST":

        form = PokemonForm(request.POST)

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


    # ======================================================
    # editar pokemon no form
    # ======================================================

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

            return redirect("home")

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


    # ======================================================
    # deletar pokemon no form
    # ======================================================

def deletar_pokemon(request, id):

    pokemon = get_object_or_404(
        Pokemon,
        id=id
    )

    if request.method == "POST":

        pokemon.delete()

        return redirect("home")

    return render(
        request,
        "confirmar_exclusao.html",
        {
            "pokemon": pokemon
        }
    )




    # ======================================================
    # listar pokemon no form
    # ======================================================

def listar_pokemon(request):

    pokemons = Pokemon.objects.all()

    return render(
        request,
        "listar_pokemon.html",
        {
            "pokemons": pokemons
        }
    )