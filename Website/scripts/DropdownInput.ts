

class DropdownInput {

    title: HTMLDivElement;
    inputField: HTMLInputElement;
    dropdown: HTMLUListElement;

    constructor(titleElement: HTMLDivElement,
                inputFieldElement: HTMLInputElement,
                dropdownElement: HTMLUListElement)
    {
        this.title = titleElement;
        this.inputField = inputFieldElement;
        this.dropdown = dropdownElement;

        this.updateDropdownEvents();
        this.addDropdownEvent();
    }

    private updateDropdownEvents()
    {
        let dropdownItems = this.dropdown.querySelectorAll("li");
        let valueArray = [];

        dropdownItems.forEach((item) => {
            valueArray.push(item.textContent);
        });

        this.inputField.addEventListener('input', () => {
            this.dropdown.classList.add('open');
            let inputValue = this.inputField.value;
            if (inputValue.length > 0) {
                for (let j = 0; j < valueArray.length; j++) {
                    if (!(inputValue.substring(0, inputValue.length)
                        === valueArray[j].substring(0, inputValue.length))) {
                        dropdownItems[j].classList.add('closed');
                    } else {
                        dropdownItems[j].classList.remove('closed');
                    }
                }
            }
            else {
                for (let i = 0; i < dropdownItems.length; i++) {
                    dropdownItems[i].classList.remove('closed');
                }
            }
        });

        dropdownItems.forEach((item) => {
            item.addEventListener('click', () => {
                this.inputField.value = item.textContent;
                dropdownItems.forEach((dropdown) => {
                    dropdown.classList.add('closed');
                });
            });
        });

        let origPlaceHolder = this.inputField.placeholder;

        this.inputField.addEventListener('focus', () => {
            this.inputField.placeholder = '输入以筛选';
            this.dropdown.classList.add('open');
            dropdownItems.forEach(function (dropdown) {
                dropdown.classList.remove('closed');
            });
        });

        this.inputField.addEventListener('blur', () => {
            this.inputField.placeholder = origPlaceHolder;
            this.dropdown.classList.remove('open');
        });
    }

    private addDropdownEvent()
    {
        document.addEventListener('click', (evt) => {
            let isDropdown = this.dropdown.contains(<Node>evt.target);
            let isInput = this.inputField.contains(<Node>evt.target);
            if (!isDropdown && !isInput)
                this.dropdown.classList.remove('open');
        });
    }

    update(newFields: string[], auto: boolean = false)
    {
        this.dropdown.innerHTML = "";
        if (auto) {
            let autoLi = document.createElement('li');
            autoLi.innerText = '[自动]';
            this.dropdown.appendChild(autoLi);
        }
        newFields.forEach((cat: string) =>
        {
            let li = document.createElement('li');
            li.innerText = cat;
            this.dropdown.appendChild(li);
        });

        this.updateDropdownEvents();
    }
}