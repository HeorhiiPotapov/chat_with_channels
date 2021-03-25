function getFile() {
    document.getElementById("file-form").click();
}

let input = document.querySelector('input[type=file]');

let file;
function newFile() {
    file = input.files[0]
    return file
}

// input.onchange = function () {
//     let reader = new FileReader();
//     reader.onloadend = function () {
//         let fileObj = new newFile();
//         let size = fileObj.size
//         chatSocket.send(JSON.stringify({
//             'option': 'upload_request',
//             'file_size': size,
//         }))
//     }
//     reader.readAsArrayBuffer(file)
// }

// function loadFile(index) {
//     let chunkSize = 524288;
//     let end = index + chunkSize;
//     if (index >= file.size) {
//         return;
//     } else if (end > file.size) {
//         end = file.size;
//     }
//     chatSocket.send(file.slice(index, end))
// }


// new code ===============================


function parseFile(file, callback) {
    var fileSize = file.size;
    var chunkSize = 64 * 1024; // bytes
    var offset = 0;
    var self = this; // we need a reference to the current object
    var chunkReaderBlock = null;

    var readEventHandler = function (evt) {
        if (evt.target.error == null) {
            offset += evt.target.result.length;
            callback(evt.target.result); // callback for handling read chunk
        } else {
            console.log("Read error: " + evt.target.error);
            return;
        }
        if (offset >= fileSize) {
            console.log("Done reading file");
            return;
        }

        // of to the next chunk
        chunkReaderBlock(offset, chunkSize, file);
    }

    chunkReaderBlock = function (_offset, length, _file) {
        var r = new FileReader();
        var blob = _file.slice(_offset, length + _offset);
        r.onload = readEventHandler;
        r.readAsArrayBuffer(blob);
    }

    // now let's start the read with the first block
    chunkReaderBlock(offset, chunkSize, file);
}