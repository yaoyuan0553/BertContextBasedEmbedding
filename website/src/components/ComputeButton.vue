<template>
    <button ref="computeButton" class="compute-ranking"
            data-label="计算" @click="compute" @keyup.enter="compute">计算</button>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class ComputeButton extends Vue {
    public $refs!: {
        computeButton: HTMLButtonElement;
    };

    public compute(e: Event) {
        console.log('blah');
        this.loading(e);
        setTimeout(() => this.reset(), 2000);
    }

    public reset(callback?: () => void) {
        this.$refs.computeButton.classList.remove('loading');
        this.$refs.computeButton.removeAttribute('disabled');
        if (callback !== undefined) {
            callback();
        }
    }

    public registerGlobalEnterKey()
    {
        document.onkeyup = (e: KeyboardEvent) => {
            if (e.key === 'Enter') {
                this.$refs.computeButton.click();
            }
        };
    }

    private loading(e: Event) {
        e.preventDefault();
        e.stopPropagation();
        this.$refs.computeButton.classList.add('loading');
        this.$refs.computeButton.setAttribute('disabled', 'disabled');
    }
}
</script>

<style scoped>
button.compute-ranking {
    left: 50%;
    width: 10rem;
    height: inherit;
    margin-top: 10vh;
    position: absolute;
    border:0;
    padding:0;
    cursor:pointer;
    font-size:1rem;
    font-weight:bold;
    color:rgba(0,0,0,0);
    background:transparent;
    border-radius:.25rem;
    -webkit-tap-highlight-color: rgba(0,0,0,0);
    -webkit-touch-callout: none;
}

button.compute-ranking,
button.compute-ranking:after,
button.compute-ranking:before {
    padding:.6875rem 2rem;
    -webkit-transition:-webkit-transform 0.75s,background-color .125s;
    -moz-transition:-moz-transform 0.75s,background-color .125s;
    -ms-transition:-ms-transform 0.75s,background-color .125s;
    transition:transform 0.75s,background-color .125s;
    -webkit-transform-style:preserve-3d;
    -moz-transform-style:preserve-3d;
    -ms-transform-style:preserve-3d;
    transform-style:preserve-3d;
}

button.compute-ranking:after,
button.compute-ranking:before {
    position:absolute;
    top:0;
    bottom:0;
    left:0;
    right:0;
    border-radius:.25rem;
    -webkit-backface-visibility:hidden;
    -moz-backface-visibility:hidden;
    -ms-backface-visibility:hidden;
    backface-visibility:hidden;

}

button.compute-ranking:before {
    z-index:2;
    color:#fff;
    background-color:#3e87ec;
    content:attr(data-label);
}

button.compute-ranking:after {
    z-index:1;
    background-color:#999;
    background-repeat:no-repeat;
    background-position:center center;
    background-image:url(data:image/gif;base64,R0lGODlhEAAQAPIAAJmZmf///7CwsOPj4////9fX18rKysPDwyH+GkNyZWF0ZWQgd2l0aCBhamF4bG9hZC5pbmZvACH5BAAKAAAAIf8LTkVUU0NBUEUyLjADAQAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQACgABACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkEAAoAAgAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkEAAoAAwAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkEAAoABAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQACgAFACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQACgAGACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAAKAAcALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA==);
    -webkit-transform:rotateX(180deg);
    -moz-transform:rotateX(180deg);
    -ms-transform:rotateX(180deg);
    transform:rotateX(180deg);
    content:'';
}

button.compute-ranking:active:before {
    background-color:#3571c8;
}

button.compute-ranking.loading {
    -webkit-transform:rotateX(180deg);
    -moz-transform:rotateX(180deg);
    -ms-transform:rotateX(180deg);
    transform:rotateX(180deg);
}

</style>
