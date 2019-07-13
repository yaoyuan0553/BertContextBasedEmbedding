import $ = require("jquery");
import KeyPressEvent = JQuery.KeyPressEvent;

class ComputeButton {
    button: HTMLButtonElement;

    private loading(e: Event)
    {
        e.preventDefault();
        e.stopPropagation();
        this.button.classList.add('loading');
        this.button.setAttribute('disabled', 'disabled');
    }

    constructor(identifier: string, callbackOnClick?: () => void)
    {
        this.button = <HTMLButtonElement>$(identifier)[0];
        this.button.onclick = (e: Event) => {
            this.loading(e);
            if (callbackOnClick !== undefined)
                callbackOnClick();
        };

        // bind the button to enter key as well
        $('body').keypress((e: KeyPressEvent) => {
            if (e.keyCode === 13) {
                e.preventDefault();
                this.button.click();
            }
        });
    }

    reset(callback?: () => void)
    {
        this.button.classList.remove('loading');
        this.button.removeAttribute('disabled');
        if (callback !== undefined)
            callback();
    }
}