<template>
    <div class="expandable-menu">
        <input type="checkbox">
        <span></span>
        <span></span>
        <span></span>
        <div class="options">
            <li><a href="#">Home</a></li>
            <li><a href="#">Design</a></li>
            <li><a href="#">Development</a></li>
            <li><a href="#">SEO</a></li>
            <li><a href="#">Contact</a></li>
            <li><a href="#">哈哈</a> </li>
        </div>
    </div>
</template>

<script>

import {Component, Vue} from 'vue-property-decorator';

@Component
export default class ExpandableMenu extends Vue {

}

</script>

<style scoped>

/** code by webdevtrick ( https://webdevtrick.com ) **/

.expandable-menu, .options {
    display: flex;
    justify-content: center;
    align-items: center;
}
.expandable-menu {
    position: relative;
    background-color: #fff;
    width: 80px;
    padding: 20px;
    transition: 0.5s;
    border-radius: 50px;
    overflow: hidden;
    box-shadow: 0 8px 15px rgba(0,0,0,.2);
}
.options {
    margin: 0;
    padding: 0;
    width: 0;
    overflow: hidden;
    transition: 0.5s;
}
.expandable-menu input:checked ~ .options {
    width: 700px;
}
.options li {
    list-style: none;
    margin: 0 10px;
}
.options li a {
    text-decoration: none;
    color: #666;
    text-transform: uppercase;
    font-weight: 600;
    transition: 0.5s;
}
.options li a:hover {
    color: #161919;
}
.expandable-menu input {
    width: 40px;
    height: 40px;
    cursor: pointer;
    opacity: 0.5;
}
.expandable-menu span {
    position: absolute;
    /*left: 30px;*/
    left: 48.5%;
    width: 30px;
    height: 4px;
    border-radius: 50px;
    background-color: #666;
    pointer-events: none;
    transition: 0.5s;
}
.expandable-menu input:checked ~ span {
    background-color: #FF4D50;
}
.expandable-menu span:nth-child(2) {
    transform: translateY(-8px);
}
.expandable-menu input:checked ~ span:nth-child(2) {
    transform: translateY(0) rotate(-45deg);
}
.expandable-menu span:nth-child(3) {
    transform: translateY(8px);
}
.expandable-menu input:checked ~ span:nth-child(3) {
    transform: translateY(0) rotate(45deg);
}
.expandable-menu input:checked ~ span:nth-child(4) {
    display: none;
}

</style>