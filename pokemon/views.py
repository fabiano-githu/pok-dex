
from django.shortcuts import render
import requests
from deep_translator import GoogleTranslator


def home(request):

    url = "https://pokeapi.co/api/v2/pokemon?limit=20"

    response = requests.get(url)
    data = response.json()

    pokemons = []

    for item in data['results']:

        # Dados principais do Pokémon
        detail = requests.get(item['url']).json()

        # Dados da espécie
        species = requests.get(detail['species']['url']).json()


        # ==========================================
        # BUSCA A DESCRIÇÃO
        # ==========================================

        descricao = ""

        # Primeiro tenta português
        for texto in species['flavor_text_entries']:

            if texto['language']['name'] == 'pt':

                descricao = texto['flavor_text']

                break


        # Se não encontrou português, pega inglês
        if not descricao:

            for texto in species['flavor_text_entries']:

                if texto['language']['name'] == 'en':

                    descricao = texto['flavor_text']

                    break


        # Remove quebras de linha
        descricao = descricao.replace('\n', ' ').replace('\f', ' ')


        # ==========================================
        # TRADUZ PARA PORTUGUÊS
        # ==========================================

        if descricao:

            try:

                descricao = GoogleTranslator(
                    source='auto',
                    target='pt'
                ).translate(descricao)

            except Exception:

                # Se a tradução falhar,
                # mantém o texto original
                pass


        # ==========================================
        # CRIA O POKÉMON
        # ==========================================

        pokemon = {
            

            'nome': detail['name'].capitalize(),

            #'imagem': detail['sprites']['front_default'],

            'imagem': detail['sprites']['other']['official-artwork']['front_default'],

            'id': detail['id'],

            'descricao': descricao,

            'peso': detail['weight'] / 10,

            'altura': detail['height'] / 10

        }


        pokemons.append(pokemon)


    return render(
        request,
        'home.html',
        {'pokemons': pokemons}
    )


def detalhes(request, id):

    url = f"https://pokeapi.co/api/v2/pokemon/{id}"

    response = requests.get(url)

    detail = response.json()

    pokemon = {
        'id': detail['id'],
        'nome': detail['name'].capitalize(),
        'imagem': detail['sprites']['front_default'],
    }

    return render(
        request,
        'detalhes.html',
        {'pokemon': pokemon}
    )
