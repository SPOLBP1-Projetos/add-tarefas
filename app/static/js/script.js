// Aguarda o documento HTML ser completamente carregado
document.addEventListener('DOMContentLoaded', function(){

    // Seleiona todos os checkboxes de tarefas
    document.querySelectorAll('check-tarefa').forEach(checkbox => {

        // Adiciona um "Ouvinte" para o evento de mudança (marcar/desmarcar)
        checkbox.addEventListener('change', function(){
            const tarefaId = this.dataset.tarefaId
            const textoTarefa = document.getElementById(`texto-tarefa-$(tarefaId)`)

            fetch(`/tarefa/concluir/$(tarefaId)`, {
                method: 'POST'
            })
            .then(response => response.json()) // Converte a resposta do servidor para JSON
            .then(data => {
                // Se a resposta do servidor for de sucesso..
                if (data.status === 'sucesso') {
                    // Adiciona ou remove a classe CSS que risca o texto
                    textoTarefa.classList.toggle('concluida', data.concluida)
                }
            })
            .catch(error => console.error('Houve um erro na aquisição AJAX:', error))
        })
    })
})