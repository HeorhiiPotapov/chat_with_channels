let input = document.querySelector('input[type=file]');
let fileFormSubmit = document.querySelector('#chat-message-submit');

function getFile() {
    document.getElementById("file-form").click();
}

input.onchange = function () {
    let file = input.files[0];
    let reader = new FileReader();

    reader.onloadend = function () {
        let b64 = reader.result.replace(/^data:.+;base64,/, '');
        let format = reader.result.substring("data:image/".length, reader.result.indexOf(";base64"));
        fileFormSubmit.addEventListener('click', function () {
            if (input.value != '') {
                chatSocket.send(JSON.stringify({
                    'option': 'image',
                    'format': format,
                    'value': b64,
                }))
            };

            input.value = '';
        })
    };
    reader.readAsDataURL(file);
};