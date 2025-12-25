// Функция для получения токена из meta-тега
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

$(document).ready(function() {
    // Обработчик для лайка/дизлайка вопроса
    $(document).on('click', '.like-btn[data-question-id], .dislike-btn[data-question-id]', function(e) {
        e.preventDefault();
        var btn = $(this);
        var questionId = btn.data('question-id');
        var voteType = btn.data('type');

        $.ajax({
            url: window.djangoUrls.toggle_question_vote,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            data: {
                question_id: questionId,
                type: voteType
            },
            success: function(response) {
                if (response.success) {
                    $('#score-' + questionId).text(response.new_score);
                }
            },
            error: function(xhr) {
                var errorMessage = 'Произошла ошибка';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                alert('Ошибка: ' + errorMessage);
            }
        });
    });

    // Обработчик для лайка/дизлайка ответа
    $(document).on('click', '.like-btn[data-answer-id], .dislike-btn[data-answer-id]', function(e) {
        e.preventDefault();
        var btn = $(this);
        var answerId = btn.data('answer-id');
        var voteType = btn.data('type');

        $.ajax({
            url: window.djangoUrls.toggle_answer_vote,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            data: {
                answer_id: answerId,
                type: voteType
            },
            success: function(response) {
                if (response.success) {
                    $('#score-answer-' + answerId).text(response.new_score);
                }
            },
            error: function(xhr) {
                var errorMessage = 'Произошла ошибка';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                alert('Ошибка: ' + errorMessage);
            }
        });
    });

    // Обработчик для отметки "правильный ответ"
    $(document).on('click', '.mark-correct-btn', function(e) {
        e.preventDefault();
        var btn = $(this);
        var answerId = btn.data('answer-id');

        $.ajax({
            url: window.djangoUrls.mark_answer_correct,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            data: {
                answer_id: answerId
            },
            success: function(response) {
                if (response.success) {
                    // Скрываем все кнопки "Отметить как правильный"
                    $('.mark-correct-btn').hide();
                    // Меняем текущую кнопку на зелёную
                    btn.removeClass('btn-outline-primary').addClass('btn-success').text('✅ Правильный ответ (нажмите, чтобы снять)').removeClass('mark-correct-btn').addClass('unmark-correct-btn');
                }
            },
            error: function(xhr) {
                var errorMessage = 'Произошла ошибка';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                alert('Ошибка: ' + errorMessage);
            }
        });
    });

    // Обработчик для снятия отметки "правильный ответ"
    $(document).on('click', '.unmark-correct-btn', function(e) {
        e.preventDefault();
        var btn = $(this);
        var answerId = btn.data('answer-id');

        $.ajax({
            url: window.djangoUrls.unmark_answer_correct,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            data: {
                answer_id: answerId
            },
            success: function(response) {
                if (response.success) {
                    // Меняем кнопку обратно на обычную
                    btn.removeClass('btn-success unmark-correct-btn').addClass('btn-outline-primary mark-correct-btn').text('Отметить как правильный');
                }
            },
            error: function(xhr) {
                var errorMessage = 'Произошла ошибка';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                alert('Ошибка: ' + errorMessage);
            }
        });
    });
});