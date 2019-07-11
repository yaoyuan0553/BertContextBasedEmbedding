<template>
    <form class="dropdown-input">
        <div class="inputTitle">{{ title }}</div>
        <input ref="inputField" class="chosen-value" type="text" value="" :placeholder="placeholder" @keypress.enter.prevent/>
        <ul ref="dropdown" class="value-list"></ul>
    </form>
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator';
import InputElement from './InputElement'

@Component
export default class DropdownInput extends Vue {
    $refs!: {
        inputField: HTMLInputElement,
        dropdown: HTMLUListElement
    };

    @Prop() private title!: string;
    @Prop() private placeholder!: string;

    value() {
        return this.$refs.inputField.value;
    }

    mounted()
    {
        this.updateDropdownEvents();
        this.addDropdownEvent();
    }

    private addDropdownEvent()
    {
        document.addEventListener('click', (evt) => {
            let isDropdown = this.$refs.dropdown.contains(<Node>evt.target);
            let isInput = this.$refs.inputField.contains(<Node>evt.target);
            if (!isDropdown && !isInput)
                this.$refs.dropdown.classList.remove('open');
        });
    }

    private updateDropdownEvents() {
        let dropdownItems = this.$refs.dropdown.querySelectorAll("li");
        let valueArray: string[] = [];

        dropdownItems.forEach((item) => {
            if (item.textContent)
              valueArray.push(item.textContent);
        });

        this.$refs.inputField.addEventListener('input', () => {
            this.$refs.dropdown.classList.add('open');
            let inputValue = this.$refs.inputField.value;
            if (inputValue.length > 0) {
                for (let j = 0; j < valueArray.length; j++) {
                    if (!(inputValue.substring(0, inputValue.length)
                        === valueArray[j].substring(0, inputValue.length))) {
                        dropdownItems[j].classList.add('closed');
                    } else {
                        dropdownItems[j].classList.remove('closed');
                    }
                }
            } else {
                for (let i = 0; i < dropdownItems.length; i++) {
                    dropdownItems[i].classList.remove('closed');
                }
            }
        });
        dropdownItems.forEach((item) => {
            item.addEventListener('click', () => {
                this.$refs.inputField.value = item.textContent as string;
                dropdownItems.forEach((dropdown) => {
                    dropdown.classList.add('closed');
                });
            });
        });

        let origPlaceHolder = this.$refs.inputField.placeholder;

        this.$refs.inputField.addEventListener('focus', () => {
            this.$refs.inputField.placeholder = '输入以筛选';
            this.$refs.dropdown.classList.add('open');
            dropdownItems.forEach(function (dropdown) {
                dropdown.classList.remove('closed');
            });
        });

        this.$refs.inputField.addEventListener('blur', () => {
            this.$refs.inputField.placeholder = origPlaceHolder;
            this.$refs.dropdown.classList.remove('open');
        });
    }

    public update(newFields: string[], auto: boolean = false)
    {
        this.$refs.dropdown.innerHTML = "";
        if (auto) {
            let autoLi = document.createElement('li');
            autoLi.innerText = '[自动]';
            this.$refs.dropdown.appendChild(autoLi);
        }
        newFields.forEach((cat: string) =>
        {
            let li = document.createElement('li');
            li.innerText = cat;
            this.$refs.dropdown.appendChild(li);
        });

        this.updateDropdownEvents();
    }
}

</script>

<style scoped>

form.dropdown-input {
}

.chosen-value,
.value-list {
    width: 200px;
}

.chosen-value {
    /* font-family: "NSimSun"; */
    font-weight: 600;
    letter-spacing: 4px;
    height: 2rem;
    font-size: 1.1rem;
    padding: 1rem;
    background-color: #FAFCFD;
    border: 3px solid transparent;
    -webkit-transition: .3s ease-in-out;
    transition: .3s ease-in-out;
}
.chosen-value::-webkit-input-placeholder {
    color: #333;
}
.chosen-value:hover {
    background-color: #FF908B;
    cursor: pointer;
}
.chosen-value:hover::-webkit-input-placeholder {
    color: #333;
}
.chosen-value:focus, .chosen-value.open {
    box-shadow: 0px 5px 8px 0px rgba(0, 0, 0, 0.2);
    outline: 0;
    background-color: #FF908B;
    color: #000;
}
.chosen-value:focus::-webkit-input-placeholder, .chosen-value.open::-webkit-input-placeholder {
    color: #000;
}

.value-list {
    margin-left: auto;
    margin-right: auto;
    list-style: none;
    margin-top: 0rem;
    box-shadow: 0px 5px 8px 0px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    max-height: 0;
    -webkit-transition: .3s ease-in-out;
    transition: .3s ease-in-out;
    opacity: 0.9;
}
.value-list.open {
    max-height: 400px;
    overflow: auto;
}

</style>

<style>

.value-list li {
    position: relative;
    height: 2rem;
    background-color: #FAFCFD;
    padding: 1rem;
    font-size: 1.1rem;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    cursor: pointer;
    -webkit-transition: background-color .3s;
    transition: background-color .3s;
    opacity: 1;
}
.value-list li:hover {
    background-color: #FF908B;
}
.value-list li.closed {
    max-height: 0;
    overflow: hidden;
    padding: 0;
    opacity: 0;
}

.inputTitle {
    color: white;
}

</style>
