fetch('/home',{
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'

    },
    body: JSON.stringify({ User: 1, ConferenceSlot: 2})
})

fetch('/booking/view',{
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ User: 1, ConferenceSlot: 2})
})