/* golbals fetch, Cookies */

console.log('hello there!')
function qs(selector) {
    return document.querySelector(selector)
}

function qsa(selector) {
    return document.querySelectorAll(selector)
}

document.addEventListener('DOMContentLoaded', function () {
    for (let form of qsa('.mark-task-complete')) {
        form.addEventListener('submit', function (event) {
            event.preventDefault()
            const csrftoken = Cookies.get('csrftoken')
            fetch(form.action, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken, 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => {
                    if (!response.ok) {
                        throw Error(response.statusText)
                    }
                    return response.json()
                })
                .then(json => {
                    qs(`#task-${form.dataset['taskid']}`).delete()
                })
        })
    }
})
