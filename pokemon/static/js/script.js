
document.addEventListener('DOMContentLoaded', function () {

    const items = document.querySelectorAll('.pokemon-item');

    const destaqueImg = document.getElementById('destaque-img');
    const destaqueNome = document.getElementById('destaque-nome');
    const destaqueId = document.getElementById('destaque-id');
    const searchInput = document.getElementById('search-input');

    // Modal
    const modalElement = document.getElementById('pokemonModal');

    const modal = new bootstrap.Modal(modalElement);

    const modalImg = document.getElementById('modal-img');
    const modalNome = document.getElementById('modal-nome');
    const modalId = document.getElementById('modal-id');
    const modalDescricao = document.getElementById('modal-descricao');


    // Pokémon selecionado
    let pokemonAtual = null;


    // Primeiro Pokémon
    if (items.length > 0) {

        const primeiro = items[0];

        pokemonAtual = {
            nome: primeiro.querySelector('.fw-semibold').textContent.trim(),
            imagem: primeiro.dataset.imagem,
            id: primeiro.dataset.id,
            descricao: primeiro.dataset.descricao || ''
        };

    }


    // Clique na lista
    items.forEach(item => {

        item.addEventListener('click', function () {

            items.forEach(i => {
                i.classList.remove('active');
            });

            this.classList.add('active');


            // Guarda o Pokémon selecionado
            pokemonAtual = {

                nome: this.querySelector('.fw-semibold').textContent.trim(),

                imagem: this.dataset.imagem,

                id: this.dataset.id,

                descricao: this.dataset.descricao || ''

            };


            // Atualiza destaque
            destaqueImg.src = pokemonAtual.imagem;

            destaqueNome.textContent = pokemonAtual.nome;

            destaqueId.textContent = '#' + pokemonAtual.id;

        });

    });


    // Pesquisa
    searchInput.addEventListener('input', function () {

        const termo = this.value.toLowerCase().trim();

        items.forEach(item => {

            const nome = item.dataset.nome;

            item.style.display =
                nome.includes(termo)
                    ? 'block'
                    : 'none';

        });

    });


    // Abre o modal
    document.getElementById('open-modal').addEventListener('click', function () {

        if (!pokemonAtual) {
            return;
        }


        // Nome
        modalNome.textContent =
            pokemonAtual.nome;


        // Imagem
        modalImg.src =
            pokemonAtual.imagem;


        // ID
        modalId.textContent =
            '#' + pokemonAtual.id;


        // Descrição
        modalDescricao.textContent =
            pokemonAtual.descricao;


        // Abre
        modal.show();

    });

});

