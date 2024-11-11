document.addEventListener('DOMContentLoaded', function () {
    const questionForm = document.getElementById('questionForm');
    const responseDiv = document.getElementById('response');

    if (questionForm) {
        questionForm.addEventListener('submit', function (e) {
            e.preventDefault();
            fetch(questionForm.action, {
                method: 'POST',
                body: new FormData(questionForm),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    responseDiv.innerHTML = `<div class="alert alert-success">${data.answer}</div>`;
                } else {
                    responseDiv.innerHTML = `<div class="alert alert-danger">Произошла ошибка.</div>`;
                }
            });
        });
    }

    const documentForm = document.getElementById('documentForm');
    const documentContentDiv = document.getElementById('documentContent');

    if (documentForm) {
        documentForm.addEventListener('submit', function (e) {
            e.preventDefault();
            fetch(documentForm.action, {
                method: 'POST',
                body: new FormData(documentForm),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    documentContentDiv.innerHTML = `<div class="alert alert-success">${data.content}</div>`;
                } else {
                    documentContentDiv.innerHTML = `<div class="alert alert-danger">Произошла ошибка.</div>`;
                }
            });
        });
    }
});
