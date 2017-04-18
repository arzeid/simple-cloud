Dropzone.options.customDropzone = {

    // Prevents Dropzone from uploading dropped files immediately
    autoProcessQueue: false,
    maxFilesize: 1024,
    parallelUploads: 25,
    clickable: "#select-button",

    init: function() {
        var submitButton = document.querySelector("#submit-button");
        var clearButton = document.querySelector("#clear-button");
        var myDropzone = this; // closure

        submitButton.addEventListener("click", function() {
            myDropzone.processQueue(); // Tell Dropzone to process all queued files.
        });
        
        clearButton.addEventListener("click", function() {
            myDropzone.removeAllFiles(true);
        });

        //this.on('success', myDropzone.processQueue.bind(myDropzone));

        // You might want to show the submit button only when 
        // files are dropped here:
        this.on("addedfile", function() {
            // Show submit button here and/or inform user to click it.
        });

        this.on("success", function(file, response) {
            this.removeFile(file);
            console.log(response);
            //createAlert('success', response.file_name+' uploaded successfully');
            addFile(response.name,response.size,response.url);
        });

        this.on("error", function(file, response) {
            this.removeFile(file);
            console.log(response);
            var message;
            if (response.hasOwnProperty('message')) {
                message = response.message;
                createAlert('warning', "Can't upload "+file.name+". "+message);
            }
            else {
                message = response;
                createAlert('error', "Can't upload "+file.name+". "+message);
            }
        });
    },

    accept: function(file, done) {
        if (file.name == "justinbieber.jpg") {
            done("Naha, you don't.");
        }
        else { done(); }
    }
};

function createAlert(level, message) {
    var s1 = '<div class="alert ';
    var s2 = '"><span class="closebtn">&times;</span><strong>';
    var s3 = '! </strong>'; 
    var s4 = '</div>';
    var html = s1+level+s2+level.toUpperCase()+s3+message+s4;
    $("#notification-zone").prepend(html);
}

function addFile(name,size,url) {
    var s1 = '<div class="file-info"><a href="';
    var s2 = '" target="_blank"><p class="leftalign">';
    var s3 = '<span class="rightalign"><span class="file-size">';
    var s4 = '</span><span class="delete-button">&times;</span>';
    var s5 = '</span></p></a></div>';
    var html = s1+url+s2+name+s3+size+s4+s5;
    $("#uploaded-files").prepend(html);
}

function deleteFile(url,div) {
    $.ajax({
        type:"DELETE",
        url:url,
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success:function (response) {
            div.remove();
            createAlert('success', response.message);
        },
        error: function (xhr, status, error) {
            createAlert('error', jQuery.parseJSON(xhr.responseText).message);
        }
    });
}

$("#notification-zone").on("click", ".closebtn", function() {
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
});

$("#uploaded-files").on("click", ".delete-button", function(e) {
    e.preventDefault();
    var div = this.parentElement.parentElement.parentElement;
    deleteFile(div.getAttribute("href"),div.parentElement);
});
