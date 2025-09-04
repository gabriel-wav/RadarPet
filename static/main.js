// Em static/js/main.js
(function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    if (flashMessages.length > 0) {
        const displayTime = 3000;

        setTimeout(() => {
            flashMessages.forEach(msg => {
                // Adiciona a classe que ativa a animação CSS
                msg.classList.add('fade-out');
                
                // Aguarda a animação terminar para remover o elemento
                msg.addEventListener('transitionend', () => {
                    msg.remove();
                });
            });
        }, displayTime);
    }
})();