function getTDs() {
    const url = "https://hi3ubxtqyl.execute-api.us-east-2.amazonaws.com/TallyPickensTouchdowns"
    var headers = {}

    fetch(url, {
        method: "GET",
        mode: 'cors',
        headers: headers
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(response.error)
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('messages').value = data.messages;
    })
    .catch(function(error) {
        document.getElementById('messages').value = data.messages;
    });
}