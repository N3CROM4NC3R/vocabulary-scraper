function app(){
    function deleteWord(e){
        newWordContainer = e.target.parentElement.parentElement;
        newWordContainer.remove();
    }

    function editWord(e){
        wordInput = e.target.parentElement.previousElementSibling;
        
        wordInput.removeAttribute("readonly");
        wordInput.focus();
        wordInput.addEventListener("focusout",(e)=>{
            e.target.setAttribute("readonly",null);
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

    addWordButton = document.getElementById("new-word-button");
    
    addWordButton.addEventListener("click",addWord);

};app();