function app(){
    function deleteWord(e){
        newWordContainer = e.target.parentElement.parentElement;
        newWordContainer.remove();
    }

    function editWord(e){
        wordInput = e.target.parentElement.previousElementSibling;
        
        wordInput.disabled = false;
        wordInput.focus();
        wordInput.addEventListener("focusout",(e)=>{
            e.target.disabled = true;
        });
    }




    function addWord(e){
        translationList = document.getElementById("translations-word-list");
        translationWordInput = document.getElementById("translation-input");

        newWordContainer = document.createElement("div");
        newWordContainer.classList.add("d-flex");
        newWordContainer.classList.add("justify-content-around");
        newWordContainer.classList.add("mt-3");
        newWordInput = document.createElement("input");
        newWordInput.classList.add("translations__input");
        newWordInput.name = ""
        newWordContent = translationWordInput.value;
        newWordInput.value = newWordContent;
        newWordInput.disabled = true;
        newWordContainer.appendChild(newWordInput);

        newWordEditButton = document.createElement("div");
        editIcon = document.createElement("i");
        editIcon.classList.add("fas"); 
        editIcon.classList.add("fa-pen");
        editIcon.classList.add("translations__icon");
        newWordEditButton.appendChild(editIcon);
        //TODO: Add the edit event to the button
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

    addWordButton = document.getElementById("new-word-button");
    
    addWordButton.addEventListener("click",addWord);

};app();