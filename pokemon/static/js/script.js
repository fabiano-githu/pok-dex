document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // ELEMENTOS DA PÁGINA
    // ==========================================

    const items = document.querySelectorAll('.pokemon-item');

    const destaqueImg = document.getElementById('destaque-img');
    const destaqueNome = document.getElementById('destaque-nome');
    const destaqueId = document.getElementById('destaque-id');

    const searchInput = document.getElementById('search-input');


    // ==========================================
    // ELEMENTOS DO MODAL
    // ==========================================

    const modalElement = document.getElementById('pokemonModal');

    const modal = new bootstrap.Modal(modalElement);

    const modalImg = document.getElementById('modal-img');
    const modalNome = document.getElementById('modal-nome');
    const modalId = document.getElementById('modal-id');

    const modalPeso = document.getElementById('modal-peso');
    const modalAltura = document.getElementById('modal-altura');

    const modalDescricao = document.getElementById('modal-descricao');


    // ==========================================
    // POKÉMON ATUAL
    // ==========================================

    let pokemonAtual = null;


    // ==========================================
    // FUNÇÃO PARA PEGAR OS DADOS
    // ==========================================

    function criarPokemon(item) {

        return {

            nome: item.querySelector('.fw-semibold')
                .textContent
                .trim(),

            imagem: item.dataset.imagem,

            id: item.dataset.id,

            descricao: item.dataset.descricao || '',

            peso: item.dataset.peso || '',

            altura: item.dataset.altura || ''

        };

    }


    // ==========================================
    // PRIMEIRO POKÉMON
    // ==========================================

    if (items.length > 0) {

        pokemonAtual = criarPokemon(items[0]);

        items[0].classList.add('active');

    }


    // ==========================================
    // CLIQUE NA LISTA
    // ==========================================

    items.forEach(item => {

        item.addEventListener('click', function () {

            // Remove seleção dos outros
            items.forEach(i => {
                i.classList.remove('active');
            });

            // Seleciona o Pokémon clicado
            this.classList.add('active');


            // Pega os dados
            pokemonAtual = criarPokemon(this);


            // ==========================================
            // ATUALIZA O DESTAQUE
            // ==========================================

            destaqueImg.src = pokemonAtual.imagem;

            destaqueImg.alt = pokemonAtual.nome;

            destaqueNome.textContent = pokemonAtual.nome;

            destaqueId.textContent = '#' + pokemonAtual.id;

        });

    });


    // ==========================================
    // PESQUISA
    // ==========================================

    searchInput.addEventListener('input', function () {

        const termo = this.value
            .toLowerCase()
            .trim();


        items.forEach(item => {

            const nome = item.dataset.nome;


            if (nome.includes(termo)) {

                item.style.display = '';

            } else {

                item.style.display = 'none';

            }

        });

    });


    // ==========================================
    // ABRIR MODAL
    // ==========================================

    const openModal = document.getElementById('open-modal');


    openModal.addEventListener('click', function () {

        // Verifica se existe Pokémon selecionado
        if (!pokemonAtual) {
            return;
        }


        // ==========================================
        // NOME
        // ==========================================

        modalNome.textContent =
            pokemonAtual.nome;


        // ==========================================
        // IMAGEM
        // ==========================================

        modalImg.src =
            pokemonAtual.imagem;

        modalImg.alt =
            pokemonAtual.nome;


        // ==========================================
        // ID
        // ==========================================

        modalId.textContent =
            '#' + pokemonAtual.id;


        // ==========================================
        // PESO
        // ==========================================

        modalPeso.textContent =
            pokemonAtual.peso;


        // ==========================================
        // ALTURA
        // ==========================================

        modalAltura.textContent =
            pokemonAtual.altura;


        // ==========================================
        // DESCRIÇÃO
        // ==========================================

        modalDescricao.textContent =
            pokemonAtual.descricao;


        // ==========================================
        // ABRE O MODAL
        // ==========================================

        modal.show();

    });

});