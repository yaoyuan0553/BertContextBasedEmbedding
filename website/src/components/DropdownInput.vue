<template>
    <form class="dropdown-input">
        <div class="inputTitle">{{ title }}</div>
        <input class="chosen-value" type="text" value="" :placeholder="placeholder" />
        <ul class="value-list"></ul>
    </form>
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class DropdownInput extends Vue {
    @Prop() private title!: string;
    @Prop() private placeholder!: string;
}

</script>

<style scoped>

form.dropdown-input {
    display: inline;
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