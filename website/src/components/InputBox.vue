<template>
    <form>
        <div class="inputTitle">{{ title }}</div>
        <input ref="inputBox" class="input-box" type="text" @keypress.enter.prevent/>
    </form>
</template>

<script lang="ts">

import { Component, Prop, Vue } from "vue-property-decorator";
import InputElement from "./InputElement"

@Component
export default class InputBox extends Vue {
    $refs!: {
        inputBox: HTMLInputElement
    };

    @Prop() private title!: string;

    value() {
        return this.$refs.inputBox.value;
    }
}

</script>

<style scoped>

input.input-box {
    font-weight: 600;
    font-size: 1.1rem;
    height: 2rem;
    padding: 1rem;
    background-color: #FAFCFD;
    border: 3px solid transparent;
    -webkit-transition: .3s ease-in-out;
    transition: .3s ease-in-out;
    width: 10ch;
}

input.input-box:hover {
    background-color: #FF908B;
    cursor: pointer;
}

div.inputTitle {
    color: white;
}

</style>