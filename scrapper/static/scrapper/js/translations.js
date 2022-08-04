function app(){
    function downloadFile(url){

        const link = document.createElement("a");
        link.href = url;

        link.click();


    }
    //Event to delete a word from the list
    function deleteWord(e){
        newWordContainer = e.target.parentElement.parentElement;
        newWordContainer.remove();
    }


    //Event to activate the input of a word from the list
    function editWord(e){
        wordInput = e.target.parentElement.previousElementSibling;
        
        wordInput.removeAttribute("readonly");
        wordInput.focus();
        wordInput.addEventListener("focusout",(e)=>{
            e.target.setAttribute("readonly",null);
        });
    }

    //Event to add a new word to the list with all its elements
    function addWord(e){
        translationList = document.getElementById("translations-word-list");
        translationWordInput = document.getElementById("translation-input");

        newWordContainer = document.createElement("div");
        newWordContainer.classList.add("d-flex");
        newWordContainer.classList.add("justify-content-around");
        newWordContainer.classList.add("mt-3");
        newWordInput = document.createElement("input");
        newWordInput.classList.add("translations__input");
        newWordInput.name = 'words[]';
        newWordInput.type = "text";
        newWordInput.classList.add("translations__input--list");
        newWordContent = translationWordInput.value;
        newWordInput.value = newWordContent;
        newWordInput.setAttribute("readonly",true);
        newWordContainer.appendChild(newWordInput);

        newWordEditButton = document.createElement("div");
        editIcon = document.createElement("i");
        editIcon.classList.add("fas"); 
        editIcon.classList.add("fa-pen");
        editIcon.classList.add("translations__icon");
        newWordEditButton.appendChild(editIcon);
        
        newWordEditButton.addEventListener("click",editWord);


        newWordContainer.appendChild(newWordEditButton)

        newWordDeleteButton = document.createElement("div");
        deleteIcon = document.createElement("i");
        deleteIcon.classList.add("fas");
        deleteIcon.classList.add("fa-trash");
        deleteIcon.classList.add("translations__icon");
        newWordDeleteButton.appendChild(deleteIcon);
        newWordDeleteButton.addEventListener("click",deleteWord);
        
        newWordContainer.appendChild(newWordDeleteButton)

        translationList.appendChild(newWordContainer);
    }

    //Function to send all data to the backend
    async function sendingData(){
        words = document.getElementsByName("words[]");
        wordList = []
        
        for(let i = 0; i < words.length; i++){
            wordList.push(words[i].value);
        }

        deckName = document.getElementById("deck_name").value;
        principalTranslation = document.getElementById("principal-translation").value;
        additionalTranslation = document.getElementById("additional-translation").value;
        compoundTranslation = document.getElementById("compound-translation").value;
        verbLocution = document.getElementById("verb-locution").value;
        
        data = {
            deck_name:deckName,
            words:wordList,
            "principal-translation":principalTranslation,
            "additional-translation":additionalTranslation,
            "compound-translation":compoundTranslation,
            "verb-locution":verbLocution
        };


        csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0];
        csrfToken = csrfToken.value
        
        let headers = new Headers({
            "X-CSRFToken":csrfToken
        });

        request_data = {
            method : 'POST',
            headers,
            body : JSON.stringify(data)
        }

        let res = await fetch("/translations",request_data);
        
        return res;
    }
    //Event when the user submits the form, therefore, he creates the deck
    async function submitWords(event){
        event.preventDefault();
        
        Swal.fire({
            html:"Are you sure you want to make a new deck?",
            background:'#1C658C',
            color:"#FFFFFF",
            confirmButtonColor: '#3B8EB9',
            preConfirm: () => {
                Swal.update({
                    "html":"Please wait<br/>Making the deck",
                    showConfirmButton:false
                });
                Swal.showLoading();
                return sendingData().then(response => {
                    if(!response.ok){
                        throw new Error(response.statusText)
                    }
                    return response.json()
                })
                .catch(error => {
                    Swal.showValidationMessage(
                        `Request failed: ${error}`
                    )
                });
    
            },
            showConfirmButton:true,
            customClass:{
                loader:"loader"
            },
            allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
            if(result.isConfirmed){
                url = result.value.downloadUrl;

                downloadFile(url);

                Swal.fire({
                    title:"Done",
                    background:'#1C658C',
                    color:"#FFFFFF",
                    confirmButtonColor: '#3B8EB9',
                });
            }
        });
    }
    
    addWordButton = document.getElementById("new-word-button");
    
    addWordButton.addEventListener("click",addWord);
    
    translationsForm = document.getElementById("translations-form");

    translationsForm.addEventListener("submit",submitWords);

};app();